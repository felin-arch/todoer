import todoist
import os

class Todoer():

    def __init__(self, todoist_api_token):
        self.token = todoist_api_token
        self.api = todoist.TodoistAPI(self.token)

    def refresh(self):
        self.api.sync(resource_types=['items', 'labels', 'projects'])

    def commit(self):
        self.api.commit()

    @property
    def items(self):
        return self.api.items.all()

    @property
    def projects(self):
        return self.api.projects.all()

    @property
    def labels(self):
        return self.api.labels.all()

    def get_label_by_name(self, name):
        return self._get_by_property(self.labels, name, 'name')

    def get_project_by_name(self, name):
        return self._get_by_property(self.projects, name, 'name')

    def get_items_by_project(self, project_id):
        items = []
        for item in self.items:
            if item['project_id'] == project_id:
                items.append(item)

        return sorted(items, key=lambda item: item['item_order'])

    def get_item_by_id(self, item_id):
        return self.api.items.get_by_id(item_id)

    def get_project_by_id(self, project_id):
        return self.api.projects.get_by_id(project_id)

    def _get_by_property(self, collection, matcher, property):
        for item in collection:
            if item[property] == matcher:
                return item

        return None


    @staticmethod
    def create():
        return Todoer(os.getenv('TODOIST_API_TOKEN'))
