from abc import ABCMeta, abstractmethod
from typing import List
from .document import Document


class Library:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, query: str, limit: int) -> List[Document]:
        """Найти подходящие документы"""

    @abstractmethod
    def fetch_content(self, id: str) -> str:
        """Получить контент документа"""
