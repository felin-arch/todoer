import logging

SKIPPED_PROJECTS = ['Inbox', 'Movies', 'Books', 'Someday', 'Lists']
NON_SEQUENTIAL_PROJECTS = ['Work', 'Personal']
SKIPPED_LABELS = ['waiting_for', 'next_action']

class NextActionFinder():

    def __init__(self, todoist):
        self._todoist = todoist
        self._logger = logging.getLogger('NextActionFinder')
        self._forbidden_labels = self._resolve_forbidden_labels(SKIPPED_LABELS)

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

    def _resolve_forbidden_labels(self, forbidden_label_names):
        forbidden_labels = []
        for label_name in forbidden_label_names:
            label = self._todoist.get_label_by_name(label_name)
            if label is not None:
                forbidden_labels.append(label['id'])

        self._logger.debug('got {0} forbidden labels'.format(len(forbidden_labels)))
        return forbidden_labels

    def _should_process_project(self, project):
        return project['name'] not in SKIPPED_PROJECTS

    def _get_next_actions_for_project(self, project):
        items = self._todoist.get_items_by_project(project['id'])
        self._logger.debug('got {0} items'.format(len(items)))
        next_actions = []
        if self._is_parallel_project(project):
            self._logger.debug('project is parallel, returning all actions')
            next_actions.extend(
                [item for item in items if self._is_next_action_candidate(item)]
            )
        else:
            self._logger.debug('project is sequential, returning first action')
            candidates = [items[0]] if len(items) is not 0 else []
            next_actions.extend(
                [item for item in candidates if self._is_next_action_candidate(item)]
            )

        self._logger.debug('added {0} next actions'.format(len(next_actions)))
        return next_actions

    def _is_next_action_candidate(self, item):
        if item['due_date'] is not None:
            self._logger.debug('drop {0}, reason: due_date'.format(item['content']))
            return False

        if self._has_forbidden_label(item):
            self._logger.debug('drop {0}, reason: label'.format(item['content']))
            return False

        return True

    def _is_parallel_project(self, project):
        return project['name'] in NON_SEQUENTIAL_PROJECTS

    def _has_forbidden_label(self, item):
        for forbidden_label in self._forbidden_labels:
            if forbidden_label in item['labels']:
                return True

        return False
