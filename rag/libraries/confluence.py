import os
from atlassian import Confluence as ConfluenceBase
from rag import Document, Library
from typing import List


class Confluence(Library):
    def __init__(self, url: str, username: str, password: str, cache: str):
        self.confluence = ConfluenceBase(url=url, username=username, password=password)
        self.cache = cache
        os.makedirs(self.cache, exist_ok=True)

    def search(self, query: str, limit: int) -> List[Document]:
        # Normalize the query to avoid searching for irrelevant text
        query = query.strip().lower()

        print("Query: " + query)

        response = self.confluence.cql(
            cql=f'siteSearch ~ "{query}" AND type in ("page")',
            start=0,
            limit=limit,
            include_archived_spaces='false'
        )

        results = response.get('results', [])
        print("Count results: " + len(results).__str__())

        # Extract links and content details
        sources = []
        for result in results:
            content = result.get('content', {})
            id = content.get('id')
            if id is None:
                continue

            text = self.fetch_content(id)
            if text == '':
                print("Empty page " + id)
                continue

            sources.append(Document(
                id=id,
                content=text,
                title=content.get('title'),
                link=self.confluence.url + '/pages/viewpage.action?pageId=' + id
            ))

        return sources

    def fetch_content(self, id: str) -> str:
        file_path = os.path.join(self.cache, id + '.html')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                html = file.read()
                print("Get page " + id + " from cache")
        else:
            response = self.confluence.get_page_by_id(page_id=id, expand='body.storage')
            html = response.get('body', {}).get('storage', {}).get('value')
            print("Load page " + id)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(html)
                print("Cache page " + id)
                file.close()

        return html
