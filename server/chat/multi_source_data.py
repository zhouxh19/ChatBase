import os
import re

from fastapi import Body, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from configs import (LLM_MODELS, TEMPERATURE)
from configs.file_config import MULTI_SOURCE_FILES_PATH
from server.utils import wrap_done, get_ChatOpenAI, BaseResponse, execute_code, save_file
from server.utils import get_prompt_template
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable
import asyncio
from langchain.prompts.chat import ChatPromptTemplate
from server.chat.utils import History
import json
import pandas as pd
from datetime import datetime
import csv


def save_to_csv(result, filename):
    name = f"{filename}.csv"
    column_names = result["column_names"]
    data = result["data"]
    with open(os.path.join(MULTI_SOURCE_FILES_PATH, name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        for row in data:
            writer.writerow(row)

def run_code(code: str = Body(..., description="用户输入", examples=[""]),
             filePaths: str = Body(default=..., description="文件地址")):
    print("code: ", code)
    print("filename: ", filePaths)
    file_names = all_file_names(json.loads(filePaths))
    merged_name = '&'.join(filter(lambda name: name != "", file_names))

    result = execute_code(code)
    if result.get('status') and len(result.get('data', [])) > 0:
        current_time = datetime.now().strftime("%H-%M-%S")
        save_to_csv(result.get('data', []), current_time + '&' + merged_name)
    return BaseResponse(code=200, msg="success", data=result)

def all_file_names(file_paths):
    file_names = []
    for file_path in file_paths:
        # 使用正则表达式提取文件名部分，并去掉文件格式
        match = re.search(r"/([^/]+)\.\w+$", file_path)
        if match and len(match.groups()) >= 1:
            file_names.append(match.group(1))  # 返回匹配到的文件名（不包含格式）
        else:
            file_names.append("")  # 如果没有匹配到文件名，则返回空字符串
    return file_names

async def chat(query: str = Body(..., description="用户输入", examples=[""], ),
               model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。")):
    async def chat_iterator(
            query: str,
            model_name: str = LLM_MODELS[0]
    ) -> AsyncIterable[str]:

        callback = AsyncIteratorCallbackHandler()

        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=TEMPERATURE,
            max_tokens=None,
            callbacks=[callback],
        )

        prompt_template = '{{ input }}'
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages([input_msg])
        print("chat_prompt: ", chat_prompt)
        chain = LLMChain(prompt=chat_prompt, llm=model)
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"input": query}),
            callback.done),
        )
        answer = ""
        async for token in callback.aiter():
            answer += token
            print("answer: ", answer)
        try:
            answer = json.loads(answer)
            print("answer: ", answer)
        except Exception as e:
            print("Error: ", e)
        yield json.dumps({"answer": answer}, ensure_ascii=False)
        await task


    return StreamingResponse(
        chat_iterator(
            query=query,
            model_name=model_name),
        media_type="text/event-stream")


def all_files():
    folder_path = MULTI_SOURCE_FILES_PATH
    # 获取文件列表
    if not os.path.exists(folder_path):
        return BaseResponse(code=200, msg="NO FILES", data=[])
    file_list = os.listdir(folder_path)
    files = []
    edges = []
    # 获取去掉文件格式的文件名
    file_short_names = [file_name.split('.')[0] for file_name in file_list]
    print('=====:', file_short_names)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        header, rows = get_header_and_first_six_rows(file_path)
        file_id = file_name.split('.')[0]
        files.append({"path": file_path, "header": header, "file_name": file_name, "file_id": file_id, "rows": rows})
        if '&' in file_id:
            names = file_id.split('&')
            for name in names:
                if name in file_short_names:
                    edges.append({"source": name, "target": file_id})

    return BaseResponse(code=200, msg="success", data={"files": files, "edges": edges})


def get_header_and_first_six_rows(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, nrows=6)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path, nrows=6)
    else:
        return [], []

    df = df.where(pd.notnull(df), "")
    header = df.columns.tolist()
    data = df.values.tolist()

    return header, data


def upload_file(file: UploadFile = File(..., description="上传文件，支持多文件")):
    save_file_result = save_file(MULTI_SOURCE_FILES_PATH, file, True)
    file_path = save_file_result["data"]["file_path"]
    return BaseResponse(code=200, msg="success", data={"file_path": file_path})
