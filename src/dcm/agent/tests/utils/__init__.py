import os
import nose.plugins.skip as skip


SYSTEM_CHANGING_TEST_ENV = "SYSTEM_CHANGING_TEST"


def get_conf_file(fname="agent.conf"):
    path = os.path.dirname(__file__)
    path = os.path.dirname(path)
    return os.path.join(path, "etc", fname)


def system_changing(func):
    def inner(*args, **kwargs):
        if SYSTEM_CHANGING_TEST_ENV not in os.environ:
            raise skip.SkipTest(
                "Test %s will change your system environment.  "
                "If you are sure you want to do this (ie you are "
                "running in a disposable VM) sent the environment "
                "variable %s" % (func.__name__,
                                 SYSTEM_CHANGING_TEST_ENV))
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner