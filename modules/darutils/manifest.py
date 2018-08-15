import xml.etree.ElementTree as xml
from io import BytesIO


class Manifest:

    def __init__(self, documents, assets, runtime="sci@0.2.0"):
        self.documents = documents
        self.assets = assets
        self.runtime = runtime

    def add_document(self, document):
        self.documents.append(document)

    def add_asset(self, asset):
        self.assets.append(asset)

    def render(self):
        dar = xml.Element('dar')

        if self.documents:
            documents = xml.SubElement(dar, 'documents')
            for doc in self.documents:
                xml.SubElement(documents, 'document', attrib={
                    'id': doc.id,
                    'name': doc.name,
                    'type': doc.type,
                    'path': doc.path
                })

        if self.assets:
            assets = xml.SubElement(dar, 'assets')
            for asset in self.assets:
                xml.SubElement(assets, 'asset', attrib={
                    'id': asset.id,
                    'name': asset.name,
                    'mime_type': asset.mime_type,
                    'path': asset.path
                })

        runtime = xml.SubElement(dar, 'runtime')
        runtime.text = self.runtime

        # buffer = BytesIO()
        # # buffer.write(
        # #     '<!DOCTYPE sheet PUBLIC "DarManifest 0.1.0" "http://darformat.org/DarManifest-0.1.0.dtd">'.encode())
        # xml.ElementTree(dar).write(buffer, 'utf-8')
        #xml.ElementTree.tostring(dar, encoding='utf8', method='xml')

        # return buffer.getvalue()
        return xml.tostring(dar, encoding='unicode')

    def __str__(self):
        return self.render()


def __manifest_doctest():
    '''
    Dummy function for doctesting manifest.py.


    >>> from asset import Asset
    >>> from document import Document

    >>> a = Asset('assid', 'assname', 'assmime', 'asspath')
    >>> d = Document('docid', 'docname', 'docmime', 'docpath')
    >>> m = Manifest([], [])
    >>> m.add_asset(a)
    >>> m.add_document(d)
    >>> print(m.render())
    <dar><documents><document id="docid" name="docname" path="docpath" type="docmime" /></documents><assets><asset id="assid" mime_type="assmime" name="assname" path="asspath" /></assets><runtime>sci@0.2.0</runtime></dar>
    '''
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()