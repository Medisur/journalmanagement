# -*- coding: utf-8 -*-

def test_index_exists(client):
    '''page index exists?
    '''

    client.get('/default/index') # get a page
    assert client.status == 200
    assert "journals" in client.text.lower()
