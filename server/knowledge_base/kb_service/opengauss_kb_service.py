import json
import uuid

from server.knowledge_base.utils import KnowledgeFile
import psycopg2
from typing import List, Dict, Tuple
from langchain.schema import Document
from configs import kbs_config, SCORE_THRESHOLD, VECTOR_SEARCH_TOP_K
from server.knowledge_base.kb_service.base import KBService, EmbeddingsFunAdapter, \
    SupportedVSType
import shutil


class OpengaussKBService(KBService):

    def vs_type(self) -> str:
        return SupportedVSType.OPENGAUSS

    def connect(self):
        return psycopg2.connect(self.connection_string)

    def create_table(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id SERIAL PRIMARY KEY,
                        document TEXT,
                        cmetadata JSONB,
                        embedding vector(768)
                    );
                ''')

    def search_by_vector(self, query_vector, top_k: int):
        # 使用datavec的距离运算符进行最近邻查询
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                    SELECT id, document, cmetadata FROM {self.table_name}
                    ORDER BY embedding <-> %s
                    LIMIT %s;
                ''', (query_vector, top_k))
                results = cur.fetchall()
                return [Document(page_content=row[1], metadata=row[2]) for row in results]

    def do_init(self):
        self.connection_string = kbs_config.get("opengauss").get("connection_uri")
        self.table_name = self.kb_name
        self.create_table()

    def do_create_kb(self):
        # 创建一个新的知识库实例，如果需要的话
        pass  # 如果需要特别的逻辑来创建KB，可以在这里实现

    def do_drop_kb(self):
        # 删除整个知识库相关的数据和表格
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''DROP TABLE IF EXISTS {self.table_name};''')
            conn.commit()
            if hasattr(self, "kb_path"):
                shutil.rmtree(self.kb_path, ignore_errors=True)

    def _docs_to_embeddings(self, docs: List[Document]) -> Dict[str, List]:
        """
        Convert documents to embeddings.
        """
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]

        embed_func = EmbeddingsFunAdapter(self.embed_model)
        embeddings = [embed_func.embed_query(text) for text in texts]
        return {
            "texts": texts,
            "embeddings": embeddings,
            "metadatas": metadatas,
        }

    def do_add_doc(self, docs: List[Document], **kwargs) -> List[Dict]:
        data = self._docs_to_embeddings(docs)
        ids = []
        print(f"server.knowledge_base.kb_service.opengauss_kb_service.do_add_doc 输入的docs参数长度为:{len(docs)}")
        print("*" * 100)
        with self.connect() as conn:
            with conn.cursor() as cur:
                for text, embedding, metadata in zip(data["texts"], data["embeddings"], data["metadatas"]):
                    _id = str(uuid.uuid4())
                    cur.execute(f'''INSERT INTO {self.table_name} (document, cmetadata, embedding) VALUES (%s, %s, %s) RETURNING id;''', (text, json.dumps(metadata), embedding))
                    ids.append(_id)
            conn.commit()

        doc_infos = [{"id": _id, "metadata": metadata} for _id, metadata in zip(ids, data["metadatas"])]
        print("写入数据成功.")
        print("*"*100)
        return doc_infos

    def do_delete_doc(self, kb_file: KnowledgeFile, **kwargs):
        # 根据提供的KnowledgeFile对象删除对应的文档
        with self.connect() as conn:
            with conn.cursor() as cur:
                filepath = kb_file.filepath.replace('\\', '\\\\')  # 确保路径格式适合SQL查询
                cur.execute(
                    f"""DELETE FROM {self.table_name} WHERE cmetadata->>'source' = %s;""", (filepath,))
            conn.commit()

    def do_clear_vs(self):
        # 清空向量存储，也就是删除所有记录但不删除表本身
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM {self.table_name};')
            conn.commit()

    def do_search(self, query: str, top_k: int = VECTOR_SEARCH_TOP_K, score_threshold: float = SCORE_THRESHOLD) -> List[
        Tuple[Document, float]]:
        embed_func = EmbeddingsFunAdapter(self.embed_model)
        query_embedding = embed_func.embed_query(query)
        results = []
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'''SELECT id, document, cmetadata, l2_distance(embedding, %s) AS distance FROM {self.table_name} ORDER BY embedding <-> %s LIMIT %s;''',
                    (str(query_embedding), str(query_embedding), top_k))
                for row in cur.fetchall():
                    if row[1]:
                        doc = Document(page_content=row[1], metadata=row[2])
                        # 这里省略了实际计算距离的步骤，因为datavec不会返回距离信息
                        results.append((doc, row[3]))

        return results


if __name__ == '__main__':
    kb_service = OpengaussKBService("th_document", 'm3e-base')
    docs = kb_service.do_search("清华大学捐赠资金由哪些部门进行管理")
    results = []

    for doc in docs:
        print(doc)
        # results.append({
        #     "page_content": doc.page_content,
        #     "metadata": doc.metadata
        # })
    print(json.dumps(results))
