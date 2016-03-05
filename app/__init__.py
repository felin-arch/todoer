import logging
import os
from app.todoist import TodoistRepository
from app.plugins.nafinder import NextActionFinder

LOGLEVEL = int(os.getenv('LOGLEVEL', logging.ERROR))
LOGFORMAT = "%(asctime)s %(levelname)s '%(name)s' : %(message)s"
logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL)

NEXT_ACTION_LABEL = 'next_action'


def main():
    logger = logging.getLogger('Main')
    repo = TodoistRepository(os.getenv('TODOIST_API_TOKEN'))
    repo.sync()
    na_finder = NextActionFinder(repo)
    actions = na_finder.find_next_action_candidates()
    logger.debug('got {0} next actions'.format(len(actions)))
    # next_action_label = todoer.get_label_by_name(NEXT_ACTION_LABEL)
    # for action in actions:
    #     labels = action['labels']
    #     labels.append(next_action_label['id'])
    #     logger.debug('{0} is a next action'.format(action['content']))
        # action.update(labels=labels)
    # todoer.commit()
    pass
