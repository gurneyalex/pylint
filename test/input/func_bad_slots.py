""" Checks that classes uses valid __slots__ """

# pylint: disable=too-few-public-methods, missing-docstring

from collections import deque

__revision__ = 0

class NotIterable(object):
    def __iter_(self):
        """ do nothing """

class Good(object):
    __slots__ = ()

class SecondGood(object):
    __slots__ = []

class ThirdGood(object):
    __slots__ = ['a']

class FourthGood(object):
    __slots__ = ('a%s' % i for i in range(10))

class FifthGood(object):
    __slots__ = "a"

class SixthGood(object):
    __slots__ = deque(["a", "b", "c"])

class SeventhGood(object):
    __slots__ = {"a": "b", "c": "d"}

class Bad(object):
    __slots__ = list

class SecondBad(object):
    __slots__ = 1

class ThirdBad(object):
    __slots__ = ('a', 2)

class FourthBad(object):
    __slots__ = NotIterable()

class FifthBad(object):
    __slots__ = ("a", "b", "")
