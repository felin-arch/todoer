from app.criteria import Criterion


class TestRequireTodoistRepositoryAndSingleArgumentCriterion(Criterion):
    def applies_to(self, _):
        pass

    def __init__(self, todoist_repository, second_argument):
        pass
