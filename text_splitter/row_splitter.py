from langchain.text_splitter import CharacterTextSplitter
from typing import List


class RowSplitter(CharacterTextSplitter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def split_text(self, text: str) -> List[str]:
        text = text.replace('\n\n\n', '\n')
        text = text.replace('\n\n', '\n')
        sent_list = [i for i in text.split("\n") if i]
        return sent_list
