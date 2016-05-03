from app.criteria import Criterion
from app.logger import log


class TrueCriterion(Criterion):
    @log('True for `{item[text]}`')
    def applies_to(self, item):
        return True


class FalseCriterion(Criterion):
    @log('False for `{item[text]}`')
    def applies_to(self, item):
        return False


class AllCriterion(Criterion):
    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches all criteria?')
    def applies_to(self, item):
        return all([criterion.applies_to(item) for criterion in self.criteria])


class AnyCriterion(Criterion):
    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches any criteria?')
    def applies_to(self, item):
        return any([criterion.applies_to(item) for criterion in self.criteria])


class NotCriterion(Criterion):
    def __init__(self, criterion):
        self.criterion = criterion

    @log('`{item[text]}` not matches criterion?')
    def applies_to(self, item):
        return not self.criterion.applies_to(item)


class AnyOfCriterion(Criterion):
    def __init__(self, criterion):
        self.criterion = criterion

    @log('Any of the {item[count]} items match?')
    def applies_to(self, items):
        return any([self.criterion.applies_to(item) for item in items])
