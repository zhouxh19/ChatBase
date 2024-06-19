import chromadb
from chromadb.utils import embedding_functions

from configs import ONLINE_LLM_MODEL, CHUNK_SIZE
from server.utils import get_model_path

client = chromadb.PersistentClient(path="/Volumes/NBDATA/JobProjects/Tsinghua/Data-chat/chroma_db")
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings


class EmbFn():
    def __init__(self):
        # self.model = HuggingFaceEmbeddings(model_name='m3e-base', cache_folder='./m3e-base')

        self.model = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002",
                                                                 api_base=ONLINE_LLM_MODEL.get('openai-api').get(
                                                                     'api_base_url'),
                                                                 api_key=get_model_path(
                                                                     "text-embedding-ada-002"))

    def __call__(self, input) -> Embeddings:
        # embed the documents somehow
        embeddings = self.model.embed_documents(input)
        return embeddings


embfn = EmbFn()
collection = client.get_collection(name="create_test", embedding_function=embfn)

text = "AI4DB主要用于数据库的自治运维和管理有什么作用？"

results = collection.query(
    query_texts=[text],
    n_results=10
)

# peek = collection.peek()

# print("peek：", peek)

print("results：", results)
