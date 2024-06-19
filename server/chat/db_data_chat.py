from fastapi import Body, Request
from fastapi.responses import StreamingResponse
from configs import (LLM_MODELS, TEMPERATURE)
from server.utils import wrap_done, get_ChatOpenAI, BaseResponse
from server.utils import get_prompt_template
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable, List, Optional
import asyncio
from langchain.prompts.chat import ChatPromptTemplate
from server.chat.utils import History
import json
import pymysql


class Database:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
            port=self.port,
            charset='utf8'
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_type is not None:
            return False

    def execute_sql(self, sql):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall(), [desc[0] for desc in cur.description]
        except Exception as e:
            print(f"SQL Execution Failed: {e}")
            return [], []

    def get_all_tables(self):
        all_tables_sql = "SHOW TABLES"
        all_tables, column_names = self.execute_sql(all_tables_sql)
        tables = [table[0] for table in all_tables]
        return tables

    def get_table_ddl(self, table_name):
        ddl_sql = f"SHOW CREATE TABLE `{table_name}`"
        ddl_result, column_names = self.execute_sql(ddl_sql)
        return ddl_result[0][1]

    def get_ddl_info(self):
        tables = self.get_all_tables()
        table_ddl = []
        for table in tables:
            ddl = self.get_table_ddl(table_name=table)
            table_ddl.append({'table': table, 'ddl': ddl})
        return table_ddl


def db_ddl_info(host: str = Body(..., description="数据库地址"),
                user: str = Body(..., description="数据库用户名"),
                password: str = Body(..., description="数据库密码"),
                database: str = Body(..., description="数据库名称"),
                port: int = Body(..., description="数据库端口")):
    def request():
        with Database(host=host, user=user, password=password, database=database, port=port) as db:
            return db.get_ddl_info()

    data = request()
    return BaseResponse(code=200, msg="Success", data=data)


def db_execute_sql(host: str = Body(..., description="数据库地址"),
                   user: str = Body(..., description="数据库用户名"),
                   password: str = Body(..., description="数据库密码"),
                   database: str = Body(..., description="数据库名称"),
                   port: int = Body(..., description="数据库端口"),
                   sql: str = Body(..., description="执行语句")):
    def request():
        with Database(host=host, user=user, password=password, database=database, port=port) as db:
            return db.execute_sql(sql=sql)

    data, column_names = request()
    if len(data) >= 1:
        data = list(data)
    return BaseResponse(code=200, msg="Success", data={'column_names': column_names, 'data': data})


async def db_generate_sql(query: str = Body(..., description="用户输入", examples=[""], ),
                          ddl: str = Body(..., description="数据库DDL", examples=['']),
                          temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                          model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                          max_tokens: Optional[int] = Body(
                              None,
                              description="限制LLM生成Token数量，默认None代表模型最大值"
                          )):
    async def db_generate_sql_iterator(
            query: str,
            ddl: str,
            model_name: str = LLM_MODELS[0]
    ) -> AsyncIterable[str]:
        nonlocal max_tokens
        callback = AsyncIteratorCallbackHandler()
        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = None

        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        prompt_template = get_prompt_template("db_data_chat", 'default')
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages([input_msg])
        chain = LLMChain(prompt=chat_prompt, llm=model)

        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"context": ddl, "question": query}),
            callback.done),
        )
        answer = ""
        async for token in callback.aiter():
            answer += token
        yield json.dumps({"answer": answer}, ensure_ascii=False)
        await task

    return StreamingResponse(db_generate_sql_iterator(query=query, ddl=ddl, model_name=model_name),
                             media_type="text/event-stream")
