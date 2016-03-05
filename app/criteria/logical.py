from app.logger import log


class TrueCriterion():

    @log('True for `{item[text]}`')
    def applies_to(self, item):
        return True


class FalseCriterion():

    @log('False for `{item[text]}`')
    def applies_to(self, item):
        return False


class AllCriterion():

    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches all criteria?')
    def applies_to(self, item):
        return all(
            [criterion.applies_to(item) for criterion in self.criteria]
        )


class AnyCriterion():

    def __init__(self, criteria):
        self.criteria = criteria

    @log('`{item[text]}` matches any criteria?')
    def applies_to(self, item):
        return any(
            [criterion.applies_to(item) for criterion in self.criteria]
        )


class NegativeCriterion():

    def __init__(self, criterion):
        self._criterion = criterion

    @log('`{item[text]}` not matches criterion?')
    def applies_to(self, item):
        return not self._criterion.applies_to(item)
