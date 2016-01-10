import logging
from criterion import ItemHasLabelCriterion, AnyCriterion, ItemHasDueDateCriterion, NegativeCriterion, AllCriterion, ItemIsNthInProjectCriterion
from criterion import ProjectNameEqualsCriterion, ProjectNameStartsWithCriterion
from criterion import ItemsProjectCriterion

class NextActionFinder():

    def __init__(self, todoist):
        self._todoist = todoist
        self._logger = logging.getLogger('NextActionFinder')
        self._criterion = AllCriterion([
            NegativeCriterion(
                AnyCriterion([
                    ItemHasLabelCriterion(todoist.get_label_by_name('waiting_for')),
                    ItemHasLabelCriterion(todoist.get_label_by_name('next_action')),
                    ItemHasDueDateCriterion()
                ])
            ),
            ItemsProjectCriterion(self._todoist, NegativeCriterion(
                AnyCriterion([
                    ProjectNameEqualsCriterion('Inbox'),
                    ProjectNameStartsWithCriterion('*')
                ])
            )),
            AnyCriterion([
                ItemsProjectCriterion(self._todoist, ProjectNameStartsWithCriterion('|')),
                ItemIsNthInProjectCriterion(self._todoist, 5)
            ])
        ])

    def find_next_action_candidates(self):
        items = self._todoist.items
        return [item for item in items if self._criterion.applies_to(item)]
