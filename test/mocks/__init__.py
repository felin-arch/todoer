import unittest

class MockItem():

    def __init__(self, content='Item', labels=[],
      due_date=None, project_id=None, item_order=0):
        self.data = {
            'content': content,
            'labels': labels,
            'due_date': due_date,
            'project_id': project_id,
            'item_order': item_order
        }

    def __getitem__(self, key):
        return self.data[key]


class MockProject():

    def __init__(self, name='Project'):
        self.data = {'name': name}

    def __getitem__(self, key):
        return self.data[key]


class MockLabel():

    def __init__(self, id=1, name='Label'):
        self.data = {'name': name, 'id': id}

    def __getitem__(self, key):
        return self.data[key]
