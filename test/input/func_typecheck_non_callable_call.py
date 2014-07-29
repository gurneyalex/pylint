# pylint: disable=R0903
"""
    'E1102': ('%s is not callable',
              'Used when an object being called has been infered to a non \
              callable object'),
"""

__revision__ = None

__revision__()

def correct():
    """callable object"""
    return 1

__revision__ = correct()

class Correct(object):
    """callable object"""

class MetaCorrect(object):
    """callable object"""
    def __call__(self):
        return self

INSTANCE = Correct()
CALLABLE_INSTANCE = MetaCorrect()
CORRECT = CALLABLE_INSTANCE()
INCORRECT = INSTANCE()
LIST = []
INCORRECT = LIST()
DICT = {}
INCORRECT = DICT()
TUPLE = ()
INCORRECT = TUPLE()
INT = 1
INCORRECT = INT()

# Test calling properties. Pylint can detect when using only the
# getter, but it doesn't infer properly when having a getter
# and a setter.
class MyProperty(property):
    """ test subclasses """

class PropertyTest(object):
    """ class """

    def __init__(self):
        self.attr = 4

    @property
    def test(self):
        """ Get the attribute """
        return self.attr

    @test.setter
    def test(self, value):
        """ Set the attribute """
        self.attr = value

    @MyProperty
    def custom(self):
        """ Get the attribute """
        return self.attr

    @custom.setter
    def custom(self, value):
        """ Set the attribute """
        self.attr = value

PROP = PropertyTest()
PROP.test(40)
PROP.custom()
