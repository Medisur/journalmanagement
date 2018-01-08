# -*- coding: utf-8 -*-

def test_index_exists(client):
    '''page index exists?
    '''

    client.get('/default/index') # get a page
    assert client.status == 200
    assert "formulario con metadatos de articulo" in client.text.lower()
