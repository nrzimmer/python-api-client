#!/usr/bin/python
import requests
import urllib.parse
import sys
import os
import traceback


def tryPrint(name, obj, key, join=False):
    if key in obj:
        if join:
            print(name + ':', ', '.join(obj[key]))
        else:
            print(name + ':', obj[key])


def processDoc(doc):
    tryPrint('Titulo', doc, 'title')
    tryPrint('Autor', doc, 'author_name', True)
    tryPrint('Assunto', doc, 'subject', True)
    tryPrint('Editora', doc, 'publisher', True)
    print('URL:', 'https://openlibrary.org' + doc['key'])
    print('----------------------')


def main():
    # Check for query on the command line
    if len(sys.argv) == 1:
        print('No query value available')
        return

    # Check for ENV variable with API port
    if 'API_PORT' in os.environ:
        port = os.environ['API_PORT']
    else:
        print('No API_PORT environment variable defined')
        return

    # Prepare query string
    query = urllib.parse.quote(' '.join(sys.argv[1:]).strip())

    # Request query from API
    try:
        r = requests.get('http://localhost:' + port + '/?q=' + query)
    except:
        print('Failed to connect to the go-api')
        return

    # Check for API return code
    if r.status_code == requests.codes.ok:
        try:
            # Parse JSON response
            js = r.json()
            print('Itens encontrados:', js['numFound'],'\n')
            for doc in js['docs']:
                processDoc(doc)
        except:
            # Invalid JSON
            print('Invalid JSON received')
            traceback.print_exc()
    else:
        # API returned an error
        print('[ERROR]', r.status_code, '|', r.text.rstrip())


if __name__ == "__main__":
    main()