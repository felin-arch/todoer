from app.criteria import Criterion


class TestSingleArgumentCriterion(Criterion):
    def applies_to(self, _):
        pass

    def __init__(self, first_argument):
        pass
