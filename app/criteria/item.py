from app.criteria import Criterion, ModifierCriterion
from app.criteria.logical import AllCriterion, AnyCriterion, NotCriterion, AnyOfCriterion
from app.logger import log


class ItemHasDueDateCriterion(Criterion):
    @log('`{item[text]}` has due date?')
    def applies_to(self, item):
        return item['due_date'] is not None


class ProjectOfItemCriterion(ModifierCriterion):
    def __init__(self, todoist_repository, criterion):
        super().__init__(criterion)
        self.todoist_repository = todoist_repository

    @log('`{item[text]}` resolving project to check `{criterion.criterion.__class__.__name__}`')
    def applies_to(self, item):
        project_of_item = self.todoist_repository.get_project_by_id(item['project_id'])
        if not project_of_item:
            return False

        return self.criterion.applies_to(project_of_item)


class ItemIsNthInProjectCriterion(Criterion):
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

    def raw(self):
        return {super().name(): self.n}


class LabelsOfItemCriterion(ModifierCriterion):
    def __init__(self, todoist_repository, criterion):
        super().__init__(criterion)
        self.todoist_repository = todoist_repository

    @log('`{item[text]}` resolving labels to check `{criterion.criterion.__class__.__name__}`')
    def applies_to(self, item):
        labels = [self.todoist_repository.get_label_by_id(label_id) for label_id in item['labels']]
        labels_of_item = [label for label in labels if label is not None]
        return self.criterion.applies_to(labels_of_item)


class ItemAllCriterion(AllCriterion):
    pass


class ItemAnyCriterion(AnyCriterion):
    pass


class ItemNotCriterion(NotCriterion):
    pass


class ItemAnyOfCriterion(AnyOfCriterion):
    pass
