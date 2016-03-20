class CriterionDefinition:
    def __init__(self, klass, should_inject_todoist_repository):
        self.klass = klass
        self.should_inject_todoist_repository = should_inject_todoist_repository

    def __eq__(self, other):
        if isinstance(other, CriterionDefinition):
            return (self.klass == other.klass and
                    self.should_inject_todoist_repository == other.should_inject_todoist_repository)

        return False
