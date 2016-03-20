from app.logger import log


class ItemHasLabelCriterion:
    def __init__(self, label):
        self.label = label

    @log('`{item[text]}` has `{criterion.label[name]}` label?')
    def applies_to(self, item):
        return self.label['id'] in item['labels']


class ItemHasDueDateCriterion:
    @log('`{item[text]}` has due date?')
    def applies_to(self, item):
        return item['due_date'] is not None


class ProjectOfItemCriterion:
    def __init__(self, todoist, criterion):
        self.todoist = todoist
        self.criterion = criterion

    @log('`{item[text]}` resolving project to check `{criterion.criterion.__class__.__name__}`')
    def applies_to(self, item):
        project_of_item = self.todoist.get_project_by_id(item['project_id'])
        if not project_of_item:
            return False

        return self.criterion.applies_to(project_of_item)


class ItemIsNthInProjectCriterion:
    def __init__(self, todoist_repository, n):
        self.todoist_repository = todoist_repository
        self.n = n

    @log('`{item[text]}` is #{criterion.n} in project?')
    def applies_to(self, item):
        items_of_project = self.todoist_repository.get_items_by_project(item['project_id'])
        item_orders = list([item['item_order'] for item in items_of_project])

        index = self.n - 1
        if index >= len(item_orders):
            return False

        return item_orders[index] == item['item_order']


class LabelsOfItemCriterion:
    def __init__(self, todoist_repository, criterion):
        self.todoist_repository = todoist_repository
        self.criterion = criterion

    @log('`{item[text]}` resolving labels to check `{criterion.criterion.__class__.__name__}`')
    def applies_to(self, item):
        labels = [self.todoist_repository.get_label_by_id(label_id) for label_id in item['labels']]
        labels_of_item = [label for label in labels if label is not None]
        return self.criterion.applies_to(labels_of_item)
