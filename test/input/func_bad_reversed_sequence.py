""" Checks that reversed() receive proper argument """

# pylint: disable-msg=too-few-public-methods,no-self-use,incomplete-protocol
from collections import deque

__revision__ = 0

class GoodReversed(object):
    """ Implements __reversed__ """
    def __reversed__(self):
        return [1, 2, 3]

class SecondGoodReversed(object):
    """ Implements __len__ and __getitem__ """
    def __len__(self):
        return 3

    def __getitem__(self, index):
        return index

class BadReversed(object):
    """ implements only len() """
    def __len__(self):
        return 3

class SecondBadReversed(object):
    """ implements only __getitem__ """
    def __getitem__(self, index):
        return index

class ThirdBadReversed(dict):
    """ dict subclass """

def test():
    """ test function """
    seq = reversed()
    seq = reversed(None)
    seq = reversed([1, 2, 3])
    seq = reversed((1, 2, 3))
    seq = reversed(set())
    seq = reversed({'a': 1, 'b': 2})
    seq = reversed(iter([1, 2, 3]))
    seq = reversed(GoodReversed())
    seq = reversed(SecondGoodReversed())
    seq = reversed(BadReversed())
    seq = reversed(SecondBadReversed())
    seq = reversed(range(100))
    seq = reversed(ThirdBadReversed())
    seq = reversed(lambda: None)
    seq = reversed(deque([]))
    return seq