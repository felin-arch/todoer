from app.actions import Action


class AddLabelToItemAction(Action):
    def __init__(self, label):
        self.label = label

    def apply_to(self, item):
        if self.label['id'] not in item['labels']:
            item['labels'].append(self.label['id'])

    def raw(self):
        return {super().name(): self.label['name']}
