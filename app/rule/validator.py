import jsonschema


class RuleValidator:
    def __init__(self, schema):
        self._validator = jsonschema.Draft4Validator(
            schema, format_checker=jsonschema.FormatChecker())

    def validate_rule(self, rule):
        result = {'errors': list(self._validator.iter_errors(rule))}
        result['is_valid'] = len(result['errors']) is 0

        return result
