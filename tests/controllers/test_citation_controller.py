# -*- coding: utf-8 -*-
from gluon.html import URL
from gluon.storage import Storage
import json

def dict_to_storage(dictionary):
    """
    Converts recursively a dictionary to a storage object
    """
    new_storage = Storage(dictionary)

    def list_dicts_to_storage(st_list):
        for i, a in enumerate(st_list):
            if isinstance(a,list):
                st_list[i] = list_dicts_to_storage(a)
            elif isinstance(a,dict):
                st_list[i] = dict_to_storage(a)

        return st_list

    for key in new_storage:
        if isinstance(new_storage[key],dict):
            new_storage[key] = dict_to_storage(new_storage[key])
        elif isinstance(new_storage[key],list):
            new_storage[key] = list_dicts_to_storage(new_storage[key])
    return new_storage

def check_api_header(response_object, web2py):
    header = dict_to_storage(response_object.header)

    assert web2py.request.application in header.application
    assert 'Citations' in header.api
    assert '1' == header.version


def test_citation_to_csl_json_api(client, web2py):

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

    response_object = dict_to_storage(json.loads(client.text))
    check_api_header(response_object, web2py)

    assert response_object.data.number == '3'
    assert response_object.data.id == 'ASD1'
    assert response_object.data.issue == '2'
    assert response_object.data.type == 'article-journal'
    assert response_object.data.URL == 'http://pepe.com'
    assert response_object.data.author[0].family == 'Rodriguez'
    assert response_object.data.author[0].given == 'G.'
    assert response_object.data.author[1].family == 'Gonzales'
    assert response_object.data.author[1].given == 'Pepe'
    assert response_object.data.issued[0]['date-parts'][0] == '2017'
    assert response_object.data.issued[0]['date-parts'][1] == '6'
    assert response_object.data.issued[0]['date-parts'][2] == '2'


