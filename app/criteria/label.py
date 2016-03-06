from app.logger import log

class LabelNameEqualsCriterion():

    def __init__(self, label_name):
        self.label_name = label_name

    @log('`{item[text]}` name equals `{criterion.label_name}`?')
    def applies_to(self, item):
        return item['name'] == self.label_name
