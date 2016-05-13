from app.util import NameConverter


class Criterion:
    def applies_to(self, _):
        raise NotImplementedError()

    def name(self):
        return NameConverter.convert_criterion_name(self.__class__.__name__)

    def raw(self):
        return {self.name(): ''}


class ModifierCriterion(Criterion):
    def __init__(self, criterion):
        self.criterion = criterion

    def applies_to(self, _):
        raise NotImplementedError()

    def raw(self):
        return {super().name(): self.criterion.raw()}


class AggregateCriterion(Criterion):
    def __init__(self, criteria):
        self.criteria = criteria

    def applies_to(self, _):
        raise NotImplementedError()

    def raw(self):
        return {super().name(): list(map(lambda x: x.raw(), self.criteria))}
