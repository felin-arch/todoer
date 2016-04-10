class ActionDefinition:
    def __init__(self, klass, parameters):
        self.klass = klass
        self.parameters = parameters

    def __eq__(self, other):
        if isinstance(other, ActionDefinition):
            return (self.klass == other.klass and
                    self.parameters == other.parameters)

        return False
