from abc import ABCMeta, abstractmethod
from typing import List
from .document import Document


class Model:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, query: str, documents: List[Document]) -> str:
        """Получение ответа от модели"""