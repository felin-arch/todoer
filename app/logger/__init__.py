from functools import wraps

from .criteria import CriteriaLogger


def log(log_format):
    def log_decorator(original_method):
        @wraps(original_method)
        def method_wrapper(*args, **kwargs):
            logger = CriteriaLogger(log_format, args[0].__class__.__name__)

            logger.log_criteria(args)
            result = original_method(*args, **kwargs)
            logger.log_result(result)

            return result

        return method_wrapper

    return log_decorator
