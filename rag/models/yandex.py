from yandex_chain import YandexLLM
from .yandex_gpt import YandexEmbeddings
from typing import List
from rag import Answer, Document, Model


class Yandex(Model):
    def __init__(self, folder_id: str, api_key: str):
        self.folder_id = folder_id
        self.api_key = api_key

    def handle(self, query: str, documents: List[Document]) -> str:
        if len(documents) == 0:
            raise Exception('Empty documents')

        embedding = YandexEmbeddings(
            folder_id=self.folder_id,
            api_key=self.api_key,
            sleep_interval=1.1,
            retries=10
        )

        model = YandexLLM(folder_id=self.folder_id, api_key=self.api_key)

        answer = Answer(
            embedding=embedding,
            model=model
        )

        return answer.get(query=query, texts=documents)
