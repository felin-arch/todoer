from app.util import NameConverter


class Action:
    def apply_to(self, _):
        raise NotImplementedError()

    def name(self):
        return NameConverter.convert_action_name(self.__class__.__name__)

    def raw(self):
        return {self.name(): ''}
