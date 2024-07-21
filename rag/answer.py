from langchain_community.vectorstores import FAISS
from langchain_core.language_models.llms import LLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from typing import List
from .document import Document


class Answer:
    def __init__(self, embedding: Embeddings, model: LLM):
        self.embedding = embedding
        self.model = model

    def chunk(self, sources: List[Document]) -> List[str]:
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.HTML,
            chunk_size=2048,
            chunk_overlap=100
        )
        documents = splitter.create_documents([source.raw_text() for source in sources])
        return [doc.page_content for doc in splitter.split_documents(documents=documents)]

    def get(self, query: str, texts: List[Document]) -> str:
        context = FAISS.from_texts(self.chunk(texts), embedding=self.embedding).as_retriever()

        template = """Отвечай на вопрос кратко основываясь только на контексте: {context}
    
        Вопрос: {question}
        """

        chat = (
                {
                    "context": context,
                    "question": RunnablePassthrough()
                }
                | ChatPromptTemplate.from_template(template)
                | self.model
                | StrOutputParser()
        )

        return chat.invoke(query)
