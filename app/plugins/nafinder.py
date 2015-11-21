import logging
from app.plugins.criterion.haslabel import HasLabelCriterion
from app.plugins.criterion.any import AnyCriterion
from app.plugins.criterion.hasduedate import HasDueDateCriterion
from app.plugins.criterion.negative import NegativeCriterion

class NextActionFinder():

    def __init__(self, todoist):
        self._todoist = todoist
        self._logger = logging.getLogger('NextActionFinder')
        self._criterion = NegativeCriterion(
            AnyCriterion([
                HasLabelCriterion(todoist.get_label_by_name('waiting_for')),
                HasLabelCriterion(todoist.get_label_by_name('next_action')),
                HasDueDateCriterion()
            ])
        )

    def find_next_action_candidates(self):
        next_actions = []
        for project in self._todoist.projects:
            if self._should_process_project(project):
                self._logger.debug('processing project: {0}'.format(project['name']))
                actions = self._get_next_actions_for_project(project)
                next_actions.extend(actions)
            else:
                self._logger.debug('skipping project: {0}'.format(project['name']))

        return next_actions

    def _should_process_project(self, project):
        if project['name'] == 'Inbox':
            return False

        return not project['name'].startswith('* ')

    def _get_next_actions_for_project(self, project):
        items = self._todoist.get_items_by_project(project['id'])
        self._logger.debug('got {0} items'.format(len(items)))
        next_actions = []
        if self._is_parallel_project(project):
            self._logger.debug('project is parallel, returning all actions')
            next_actions.extend(
                [item for item in items if self._criterion.applies_to(item)]
            )
        else:
            self._logger.debug('project is sequential, returning first action')
            candidates = [items[0]] if len(items) is not 0 else []
            next_actions.extend(
                [item for item in candidates if self._criterion.applies_to(item)]
            )

        self._logger.debug('added {0} next actions'.format(len(next_actions)))
        return next_actions

    def _is_parallel_project(self, project):
        return project['name'].startswith('| ')
