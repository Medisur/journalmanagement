import json

from resource import Resource


class Archive:

    def __init__(self, version, resources=None):
        self.version = version
        self.resources = [] if not resources else resources


    def addResource(self, name, encoding, data, size, createdAt, updatedAt):
        new_resource = Resource(name, encoding, data, size, createdAt, updatedAt)
        self.resources.append(new_resource)


    def add_manifest_resource(self, encoding, data, size, createdAt, updatedAt):
        self.addResource('manifest.xml', encoding, data, size, createdAt, updatedAt)


    def add_manuscript_resource(self, encoding, data, size, createdAt, updatedAt):
        self.addResource('manuscript.xml', encoding, data, size, createdAt, updatedAt)


    def add_hex_resource(self, name, data, size, createdAt, updatedAt):
        self.addResource(name, 'hex', data, size, createdAt, updatedAt)


    def add_url_resource(self, name, url, size, createdAt, updatedAt):
        self.addResource(name, 'url', url, size, createdAt, updatedAt)


    def to_json(self):
        archive_dict = {}
        archive_dict['version'] = self.version
        archive_dict['resources'] = [vars(r) for r in self.resources]
        return json.dumps(archive_dict)

def __archive_doctest():
    '''
    Dummy function for doctesting archive.py.


    >>> a = Archive('v1')
    >>> a.add_manifest_resource('utf-8', 'esta es la data manifest', 1234, 4565467547, 988765765)
    >>> a.add_manuscript_resource('utf-8', 'esta es la data manuscript', 76578, 4565467547, 988765765)
    >>> a.add_url_resource('fig1.jpg', 'http://www.test.cu/fig1', 7657, 4565467547, 988765765)
    >>> a.add_url_resource('fig2.jpg', 'http://www.test.cu/fig2', 7657, 4565467547, 988765765)
    >>> a.add_url_resource('fig3.jpg', 'http://www.test.cu/fig3', 7657, 4565467547, 988765765)
    >>> print(a.to_json())
    {"version": "v1", "resources": [{"name": "manifest.xml", "encoding": "utf-8", "data": "esta es la data manifest", "size": 1234, "createdAt": 4565467547, "updatedAt": 988765765}, {"name": "manuscript.xml", "encoding": "utf-8", "data": "esta es la data manuscript", "size": 76578, "createdAt": 4565467547, "updatedAt": 988765765}, {"name": "fig1.jpg", "encoding": "url", "data": "http://www.test.cu/fig1", "size": 7657, "createdAt": 4565467547, "updatedAt": 988765765}, {"name": "fig2.jpg", "encoding": "url", "data": "http://www.test.cu/fig2", "size": 7657, "createdAt": 4565467547, "updatedAt": 988765765}, {"name": "fig3.jpg", "encoding": "url", "data": "http://www.test.cu/fig3", "size": 7657, "createdAt": 4565467547, "updatedAt": 988765765}]}

    '''
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
