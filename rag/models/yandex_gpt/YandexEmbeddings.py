from yandex_chain import YandexEmbeddings as BaseYandexEmbeddings
from multiprocessing import Pool


class YandexEmbeddings(BaseYandexEmbeddings):
    def embed_documents(self, texts, chunk_size=0):
        pool = Pool(processes=10)
        results = []
        for text in texts:
            results.append(pool.apply_async(BaseYandexEmbeddings.embed_document, args=(self, text)))

        return [result.get() for result in results]
