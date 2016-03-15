import logging

from app.criteria.logical import *
from app.criteria.item import *
from app.criteria.project import *
from app.criteria.label import *

class NextActionFinder():

    def __init__(self, todoist):
        self._todoist = todoist
        self._logger = logging.getLogger('NextActionFinder')
        self._criterion = AllCriterion([
            NegativeCriterion(
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
            ProjectOfItemCriterion(self._todoist, NegativeCriterion(
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

    def _build_label_criterion(self, label_name):
        label = self._todoist.get_label_by_name(label_name)
        return ItemHasLabelCriterion(label)
