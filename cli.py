#!/usr/bin/env python

import argparse
import os
import sys
import rag
from dotenv import load_dotenv

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        usage="\n\t%(prog)s -q [string] (Пользовательский вопрос)\n" +
              "\t%(prog)s -l [number] (Лимит релеватных документов для формирования векторной базы)"
    )
    parser.add_argument("-l", "--limit", metavar="NUMBERS",
                        help="Лимит релеватных документов для формирования векторной базы")

    parser.add_argument("-q", "--query",
                        help="Пользовательский вопрос")

    parser.add_argument("-v", "--verbose",
                        help="Show additional information", action="count")

    args = parser.parse_args()

    if args.query is None:
        parser.print_help()
        sys.exit(1)

    debug = os.getenv('DEBUG') == '1' or os.getenv('DEBUG').lower() == 'true'

    try:
        library = rag.Confluence(
            url=os.getenv('CONFLUENCE_URL'),
            username=os.getenv('CONFLUENCE_USER'),
            password=os.getenv('CONFLUENCE_PASSWORD'),
            cache=os.getenv('CACHE_DIR')
        )

        documents = library.search(
            query=args.query,
            limit=int(args.limit or os.getenv('DOCUMENTS_LIMIT'))
        )

        yandex = rag.Yandex(
            folder_id=os.getenv('YA_CLOUD_FOLDER_ID'),
            api_key=os.getenv('YA_CLOUD_API_KEY')
        )

        result = yandex.handle(query=args.query, documents=documents)

        print()
        print(result)
        print()
        print()

        print("Ответ сформирован на основании информации:")
        for document in documents:
            print(' - ' + document.link + ' ' + document.title)
    except Exception as error:
        if debug is True:
            raise error
        else:
            print(error)
            sys.exit(1)


if __name__ == "__main__":
    main()
