from typing import List
from langchain.document_loaders.unstructured import UnstructuredFileLoader


class RapidOCRPDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def pdf2text(filepath):
            from paddleocr import PaddleOCR
            text = ''
            ocr = PaddleOCR(use_angle_cls=True, lang="ch")
            result = ocr.ocr(filepath, cls=True)
            for idx in range(len(result)):
                res = result[idx]
                if res == None:  # 识别到空页就跳过，防止程序报错 / Skip when empty result detected to avoid TypeError:NoneType
                    print(f"[DEBUG] Empty page {idx + 1} detected, skip it.")
                    continue
                txts = [line[1][0] for line in res]
                text += "".join(txts)
            return text

        text = pdf2text(self.file_path)
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRPDFLoader(file_path="/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/数据库系统概论-第5版_完整版.pdf")
    docs = loader.load()
    print(docs)
