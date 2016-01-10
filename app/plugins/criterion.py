import logging

class AllCriterion():

    def __init__(self, criteria):
        self._logger = logging.getLogger('AllCriterion')
        self._criteria = criteria

    def applies_to(self, item):
        self._logger.debug('`%s` matches all criteria?', self._get_item_label(item))
        result = reduce(
            lambda acc, criteria: acc and criteria.applies_to(item),
            self._criteria,
            True
        )
        self._logger.debug(result)
        return result

    def _get_item_label(self, item):
        if 'content' in item.data:
            return item['content']

        if 'name' in item.data:
            return item['name']


class AnyCriterion():

    def __init__(self, criteria):
        self._logger = logging.getLogger('AnyCriterion')
        self._criteria = criteria

    def applies_to(self, item):
        self._logger.debug('`%s` matches any criteria?', self._get_item_label(item))
        result = reduce(
            lambda acc, criteria: acc or criteria.applies_to(item),
            self._criteria,
            False
        )
        self._logger.debug(result)
        return result

    def _get_item_label(self, item):
        if 'content' in item.data:
            return item['content']

        if 'name' in item.data:
            return item['name']


class NegativeCriterion():

    def __init__(self, criterion):
        self._logger = logging.getLogger('NegativeCriterion')
        self._criterion = criterion

    def applies_to(self, item):
        self._logger.debug('`%s` not matches criterion?', self._get_item_label(item))
        result = not self._criterion.applies_to(item)
        self._logger.debug(result)
        return result

    def _get_item_label(self, item):
        if 'content' in item.data:
            return item['content']

        if 'name' in item.data:
            return item['name']


class ItemHasLabelCriterion():

    def __init__(self, label):
        self._logger = logging.getLogger('ItemHasLabelCriterion')
        self._label = label

    def applies_to(self, item):
        self._logger.debug('`%s` has `%s` label?', item['content'], self._label['name'])
        result = self._label['id'] in item['labels']
        self._logger.debug(result)
        return result


class ItemHasDueDateCriterion():

    def __init__(self):
        self._logger = logging.getLogger('ItemHasDueDateCriterion')

    def applies_to(self, item):
        self._logger.debug('`%s` has due date?', item['content'])
        result = item['due_date'] is not None
        self._logger.debug(result)
        return result


class ProjectNameEqualsCriterion():

    def __init__(self, project_name):
        self._logger = logging.getLogger('ProjectNameEqualsCriterion')
        self._project_name = project_name

    def applies_to(self, project):
        self._logger.debug('`%s` name equals `%s`?', project['name'], self._project_name)
        result = project['name'] == self._project_name
        self._logger.debug(result)
        return result


class ProjectNameStartsWithCriterion():

    def __init__(self, name_fragment):
        self._logger = logging.getLogger('ProjectNameStartsWithCriterion')
        self._name_fragment = name_fragment

    def applies_to(self, project):
        self._logger.debug('`%s` starts with `%s`?', project['name'], self._name_fragment)
        result = project['name'].startswith(self._name_fragment)
        self._logger.debug(result)
        return result


class ItemsProjectCriterion():

    def __init__(self, todoist, criterion):
        self._logger = logging.getLogger('ItemsProjectCriterion')
        self._todoist = todoist
        self._criterion = criterion

    def applies_to(self, item):
        self._logger.debug('`%s` resolving project', item['content'])
        items_project = self._todoist.get_project_by_id(item['project_id'])
        self._logger.debug('`%s` resolved project as `%s`', item['content'], items_project['name'])
        self._logger.debug('`%s` matches criterion?', items_project['name'])
        result = self._criterion.applies_to(items_project)
        self._logger.debug(result)
        return result


class ItemIsNthInProjectCriterion():

    def __init__(self, todoist, n):
        self._logger = logging.getLogger('ItemsIsNthInProjectCriterion')
        self._todoist = todoist
        self._n = n

    def applies_to(self, item):
        self._logger.debug('`%s` is #%s in project?', item['content'], self._n)
        project_items = self._todoist.get_items_by_project(item['project_id'])
        item_orders = map(lambda project_item: project_item['item_order'], project_items)
        index = self._n - 1
        if index >= len(item_orders):
            return False
        result = item_orders[self._n - 1] == item['item_order']
        self._logger.debug(result)
        return result
