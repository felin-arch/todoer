import re


class NameConverter:
    @staticmethod
    def convert_criterion_name(name):
        name = NameConverter._remove_suffix(name, 'Criterion')
        return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()

    @staticmethod
    def convert_action_name(name):
        name = NameConverter._remove_suffix(name, 'Action')
        return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()

    @staticmethod
    def _remove_suffix(name, suffix):
        return re.sub('(.*){0}'.format(suffix), r'\1', name)
