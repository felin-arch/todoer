from app.criteria import Criterion, AggregateCriterion, ModifierCriterion
from app.logger import log


class TrueCriterion(Criterion):
    @log('True for `{item[text]}`')
    def applies_to(self, item):
        return True


class FalseCriterion(Criterion):
    @log('False for `{item[text]}`')
    def applies_to(self, item):
        return False


class AllCriterion(AggregateCriterion):
    def __init__(self, criteria):
        super().__init__(criteria)

    @log('`{item[text]}` matches all criteria?')
    def applies_to(self, item):
        return all([criterion.applies_to(item) for criterion in self.criteria])


class AnyCriterion(AggregateCriterion):
    def __init__(self, criteria):
        super().__init__(criteria)

    @log('`{item[text]}` matches any criteria?')
    def applies_to(self, item):
        return any([criterion.applies_to(item) for criterion in self.criteria])


class NotCriterion(ModifierCriterion):
    def __init__(self, criterion):
        super().__init__(criterion)

    @log('`{item[text]}` not matches criterion?')
    def applies_to(self, item):
        return not self.criterion.applies_to(item)


class AnyOfCriterion(ModifierCriterion):
    def __init__(self, criterion):
        super().__init__(criterion)

    @log('Any of the {item[count]} items match?')
    def applies_to(self, items):
        return any([self.criterion.applies_to(item) for item in items])
