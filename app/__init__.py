import logging
import os
from app.plugins.todoer import Todoer
from app.plugins.nafinder import NextActionFinder

LOGLEVEL = int(os.getenv('LOGLEVEL', logging.DEBUG))
LOGFORMAT = "%(asctime)s %(levelname)s '%(name)s' : %(message)s"
logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL)

NEXT_ACTION_LABEL='next_action'

def main():
    logger = logging.getLogger('Main')
    todoer = Todoer.create()
    todoer.refresh()
    na_finder = NextActionFinder(todoer)
    actions = na_finder.find_next_action_candidates()
    print actions[0]
    logger.debug('got {0} next actions'.format(len(actions)))
    next_action_label = todoer.get_label_by_name(NEXT_ACTION_LABEL)
    for action in actions:
        labels = action['labels']
        labels.append(next_action_label['id'])
        logger.debug('{0} is a next action'.format(action['content']))
        #action.update(labels=labels)
    # todoer.commit()
