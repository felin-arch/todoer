from app.criteria import Criterion
from app.criteria.logical import AllCriterion, AnyCriterion, NotCriterion, AnyOfCriterion
from app.logger import log


class LabelNameEqualsCriterion(Criterion):
    def __init__(self, label_name):
        self.label_name = label_name

    @log('`{item[text]}` name equals `{criterion.label_name}`?')
    def applies_to(self, item):
        return item['name'] == self.label_name


class LabelAllCriterion(AllCriterion):
    pass


class LabelAnyCriterion(AnyCriterion):
    pass


class LabelNotCriterion(NotCriterion):
    pass


class LabelAnyOfCriterion(AnyOfCriterion):
    pass
