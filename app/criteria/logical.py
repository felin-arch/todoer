from app.logger import log


class TrueCriterion:
    @log('True for `{item[text]}`')
    def applies_to(self, item):
        return True


class FalseCriterion:
    @log('False for `{item[text]}`')
    def applies_to(self, item):
        return False


class AllCriterion:
    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches all criteria?')
    def applies_to(self, item):
        return all(
            [criterion.applies_to(item) for criterion in self.criteria]
        )


class AnyCriterion:
    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches any criteria?')
    def applies_to(self, item):
        return any(
            [criterion.applies_to(item) for criterion in self.criteria]
        )


class NegativeCriterion:
    def __init__(self, criterion):
        self.criterion = criterion

    @log('`{item[text]}` not matches criterion?')
    def applies_to(self, item):
        return not self.criterion.applies_to(item)


class AnyOfCriterion:
    def __init__(self, criterion):
        self.criterion = criterion

    @log('Any of the {item[count]} items match?')
    def applies_to(self, items):
        return any(
            [self.criterion.applies_to(item) for item in items]
        )
