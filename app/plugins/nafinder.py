import logging

from app.criteria.item import *
from app.criteria.label import *
from app.criteria.logical import *
from app.criteria.project import *


class NextActionFinder:
    def __init__(self, todoist):
        self._todoist = todoist
        self._logger = logging.getLogger('NextActionFinder')
        self._criterion = AllCriterion([
            NotCriterion(
                AnyCriterion([
                    LabelsOfItemCriterion(self._todoist, AnyOfCriterion(
                        AnyCriterion([
                            LabelNameEqualsCriterion('waiting_for'),
                            LabelNameEqualsCriterion('next_action')
                        ])
                    )),
                    ItemHasDueDateCriterion()
                ])
            ),
            ProjectOfItemCriterion(self._todoist, NotCriterion(
                AnyCriterion([
                    ProjectNameEqualsCriterion('Inbox'),
                    ProjectNameStartsWithCriterion('*')
                ])
            )),
            AnyCriterion([
                ProjectOfItemCriterion(
                    self._todoist, ProjectNameStartsWithCriterion('|')),
                ItemIsNthInProjectCriterion(self._todoist, 1)
            ])
        ])

    def find_next_action_candidates(self):
        items = self._todoist.items
        return [item for item in items if self._criterion.applies_to(item)]
