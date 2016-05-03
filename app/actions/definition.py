class ActionDefinition:
    def __init__(self, class_, parameters):
        self.class_ = class_
        self.parameters = parameters

    def __eq__(self, other):
        if isinstance(other, ActionDefinition):
            return (self.class_ == other.class_ and
                    self.parameters == other.parameters)

        return False
