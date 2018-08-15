import json

class Resource:

    def __init__(self, name, encoding, data, size, createdAt, updatedAt):
        self.name = name
        self.encoding = encoding
        self.data = data
        self.size = size
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_json(self):
        return json.dumps(vars(self))

    def __str__(self):
        print(vars(self))
