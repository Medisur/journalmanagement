# -*- coding: utf-8 -*-
from gluon.html import URL
from gluon.storage import Storage
import json

def check_api_header(response_object, web2py):
    header = Storage(response_object.header)

    assert web2py.request.application in header.application
    assert 'Citations' in header.api
    assert '1' == header.version

def test_citation_to_csl_json_api(client, web2py):
    '''page index exists?
    '''

    vars = {
        'id': 'ASD1',
        'type': 'article-journal',
        'author': 'Rodriguez G., Gonzales Pepe',
        'issued': '2017/6/02',
        'issue': '2',
        'number': '3',
        'URL': "http://pepe.com"

    }
    url = URL('citation', 'api', 'to_csl_json', vars=vars)

    client.get(url) # get a page
    assert client.status == 200

    response_object = Storage(json.loads(client.text))

    check_api_header(response_object, web2py)
    print(response_object.data)

