class CriterionDefinition:
    def __init__(self, class_, should_inject_todoist_repository):
        self.class_ = class_
        self.should_inject_todoist_repository = should_inject_todoist_repository

    def __eq__(self, other):
        if isinstance(other, CriterionDefinition):
            return (self.class_ == other.class_ and
                    self.should_inject_todoist_repository == other.should_inject_todoist_repository)

        return False
