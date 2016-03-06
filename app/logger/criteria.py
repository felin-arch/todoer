import logging

class CriteriaLogger():
    indent = 0

    def __init__(self, log_format, logger):
        self.log_format = log_format
        self._logger = logging.getLogger(self._get_prefix() + logger)

    def log_criteria(self, criteria_call_details):
        CriteriaLogger.indent += 1
        merged = self._merge_call_details(criteria_call_details)
        self._logger.debug(self.log_format.format_map(merged))

    def log_result(self, result):
        self._logger.debug(result)
        CriteriaLogger.indent -= 1

    def _merge_call_details(self, call_details):
        item = self._get_item(call_details[1])
        return {
            'criterion': call_details[0],
            'item': item
        }

    def _get_item(self, argument):
        if isinstance(argument, list):
            return { 'count': len(argument) }

        item = argument.data.copy()
        item['text'] = self._get_item_identifier(item)
        return item

    def _get_item_identifier(self, item):
        for label in ['content', 'name']:
            if label in item:
                return item[label]

    def _get_prefix(self):
        return '| ' * CriteriaLogger.indent
