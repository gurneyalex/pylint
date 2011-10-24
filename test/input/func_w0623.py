"""Test for W0623, overwriting names in exception handlers."""

__revision__ = ''

import exceptions

class MyError(Exception):
    """Special exception class."""
    pass


def some_function():
    """A function."""
    exc = None

    try:
        {}["a"]
    except KeyError, exceptions.RuntimeError: # W0623
        pass
    except KeyError, OSError: # W0623
        pass
    except KeyError, MyError: # W0623
        pass
    except KeyError, exc: # this is fine
        print exc
    except KeyError, exc1: # this is fine
        print exc1
    except KeyError, FOO: # C0103
        print FOO


class MyOtherError(Exception):
    """Special exception class."""
    pass


exc3 = None

try:
    pass
except KeyError, exceptions.RuntimeError: # W0623
    pass
except KeyError, OSError: # W0623
    pass
except KeyError, MyOtherError: # W0623
    pass
except KeyError, exc3: # this is fine
    print exc3
except KeyError, exc4: # this is fine
    print exc4
except KeyError, OOPS: # C0103
    print OOPS
