class AddLabelAction:
    def __init__(self, label):
        self.label = label

    def apply_to(self, item):
        if self.label['id'] not in item['labels']:
            item['labels'].append(self.label['id'])
