import re


class CriterionNameConverter:
    @staticmethod
    def convert_name(name):
        name = CriterionNameConverter._remove_criterion_suffix(name)
        return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()

    @staticmethod
    def _remove_criterion_suffix(name):
        return re.sub('(.*)Criterion', r'\1', name)
