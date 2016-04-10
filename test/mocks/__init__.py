class MockItem:
    def __init__(self, content='Item', labels=None, due_date=None, project_id=None, item_order=0):
        labels = [] if labels is None else labels
        self.data = {
            'content': content,
            'labels': labels,
            'due_date': due_date,
            'project_id': project_id,
            'item_order': item_order
        }

    def __getitem__(self, key):
        return self.data[key]


class MockProject:
    def __init__(self, name='Project'):
        self.data = {'name': name}

    def __getitem__(self, key):
        return self.data[key]


class MockLabel:
    def __init__(self, label_id=1, name='Label'):
        self.data = {'name': name, 'id': label_id}

    def __getitem__(self, key):
        return self.data[key]
