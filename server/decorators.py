import logging
from functools import wraps

logger = logging.getLogger('controllers')


def logged(log_format):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            logger.debug(
                log_format % {'name': func.__name__, 'request':request, 'args': args, 'kwargs': kwargs, 'result': result}
            )
            return result
        return wrapper
    return decorator
