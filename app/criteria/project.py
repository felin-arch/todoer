from app.logger import log


class ProjectNameEqualsCriterion:
    def __init__(self, project_name):
        self.project_name = project_name

    @log('`{item[text]}` name equals `{criterion.project_name}`?')
    def applies_to(self, item):
        return item['name'] == self.project_name


class ProjectNameStartsWithCriterion:
    def __init__(self, name_prefix):
        self.name_prefix = name_prefix

    @log('`{item[text]}` starts with `{criterion.name_prefix}`?')
    def applies_to(self, project):
        return project['name'].startswith(self.name_prefix)
