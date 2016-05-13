import re


class NameConverter:
    @staticmethod
    def convert_criterion_name(name):
        name = NameConverter._remove_suffix(name, 'Criterion')
        return NameConverter.convert_to_snake_case(name)

    @staticmethod
    def convert_action_name(name):
        name = NameConverter._remove_suffix(name, 'Action')
        return NameConverter.convert_to_snake_case(name)

    @staticmethod
    def _remove_suffix(name, suffix):
        return re.sub('(.*){0}'.format(suffix), r'\1', name)

    @staticmethod
    def convert_to_snake_case(name):
        return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()
