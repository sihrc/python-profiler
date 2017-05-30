from functools import wraps
import logging

from contextlib import contextmanager
import cProfile

logger = logging.getLogger("profiler")

@contextmanager
def profile_context(path):
    logger.info("cProfile is beginning for {path}".format(path=path))
    profile = cProfile.Profile()
    profile.enable()
    yield
    profile.disable()
    logger.info("cProfile is dumping to {path}".format(path=path))
    profile.dump_stats(path)


def profiler(path=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if path is None:
                path = fn.__name__
            with profile_context(path):
                result = fn(*args, **kwargs)
            return result
        return decorated
    return wrapper
