# pylint: disable=R0903,R0201
"""Test for the invalid-name (C0103) warning."""

__revision__ = 1

import collections

def Run():
    """method without any good name"""
    class B(object):
        """nested class should not be tested has a variable"""
        def __init__(self):
            pass
    bBb = 1
    return A, bBb

def run():
    """anothrer method without only good name"""
    class Aaa(object):
        """nested class should not be tested has a variable"""
        def __init__(self):
            pass
    bbb = 1
    return Aaa(bbb)

A = None

def HOHOHOHO():
    """yo"""
    HIHIHI = 1
    print HIHIHI

class xyz(object):
    """yo"""

    zz = 'Bad Class Attribute'

    def __init__(self):
        pass

    def Youplapoum(self):
        """bad method name"""


class Derived(xyz):
    """Derived class."""
    zz = 'Not a bad class attribute'


def no_nested_args(arg1, arg21, arg22):
    """a function which had nested arguments but no more"""
    print arg1, arg21, arg22


GOOD_CONST_NAME = ''
benpasceluila = 0

class Correct(object):
    """yo"""
    def __init__(self):
        self.cava = 12
        self._Ca_va_Pas = None

V = [WHAT_Ever_inListComp for WHAT_Ever_inListComp in GOOD_CONST_NAME]

def class_builder():
    """Function returning a class object."""

    class EmbeddedClass(object):
        """Useless class."""

    return EmbeddedClass

BAD_NAME_FOR_CLASS = collections.namedtuple('Named', ['tuple'])
NEXT_BAD_NAME_FOR_CLASS = class_builder()

GoodName = collections.namedtuple('Named', ['tuple'])
ToplevelClass = class_builder()

AlsoCorrect = Correct
NOT_CORRECT = Correct


def test_globals():
    """Names in global statements are also checked."""
    global NOT_CORRECT
    global AlsoCorrect
    NOT_CORRECT = 1
    AlsoCorrect = 2
