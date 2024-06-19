from FlagEmbedding import FlagReranker
from langchain_core.documents import Document
from typing import Sequence, Dict
from collections import OrderedDict

class RerankerModel(object):
    """Document compressor that uses `Cohere Rerank API`."""
    model_name_or_path: str
    _model = None
    min_k: int

    def __init__(self, model_name_or_path: str):
        self._model = FlagReranker(model_name_or_path, use_fp16=True)

    def compress_documents(
            self,
            documents: Sequence[Document],
            query: str,
            min_k: int = 7,
    ) -> Sequence[Document]:
        if len(documents) == 0:  # to avoid empty api call
            return []
        doc_list = list(documents)
        _docs = [d.page_content for d in doc_list]
        scores = [self._model.compute_score([query, _doc], normalize=True) for _doc in _docs]
        sorted_indices_and_docs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        # 20,30，40 ， 0.1 0.,2
        contexts = OrderedDict()  # 使用有序字典保持插入顺序且避免重复
        base = 0.1
        while len(contexts) < min_k and len(contexts) < len(doc_list):
            for i, score in sorted_indices_and_docs:
                if score > base and i not in contexts:
                    contexts[i] = doc_list[i]
            base /= 2  # 减半基线分数

        print("contexts length:", len(contexts))
        return list(contexts.values())
