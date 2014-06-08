"""test for Python 3 string formatting error
"""
# pylint: disable=too-few-public-methods, import-error
from missing import Missing

__revision__ = 1

class Custom(object):
    """ Has a __getattr__ """
    def __getattr__(self):
        return self

class Test(object):
    """ test format attribute access """
    custom = Custom()
    ids = [1, 2, 3, [4, 5, 6]]

class Getitem(object):
    """ test custom getitem for lookup access """
    def __getitem__(self, index):
        return 42

class ReturnYes(object):
    """ can't be properly infered """
    missing = Missing()

def pprint():
    """Test string format """
    print "{{}}".format(1)
    print "{} {".format()
    print "{} }".format()
    print "{0} {}".format(1, 2)
    print "{0} {1}".format(1, 2)
    print "{0} {1} {a}".format(1, 2, 3)
    print "{a} {b}".format(a=1, c=2)
    print "{} {a}".format(1, 2)
    print "{} {}".format(1)
    print "{} {}".format(1, 2, 3)
    print "{a} {b} {c}".format()
    print "{} {}".format(a=1, b=2)
    print "{a} {b}".format(1, 2)
    print "{0!r:20}".format("Hello")
    print "{!r:20}".format("Hello")
    print "{a!r:20}".format(a="Hello")
    print "{a.test}".format(a=Custom())
    print "{a.__len__}".format(a=[])
    print "{a.ids.__len__}".format(a=Test())
    print "{a.ids.__len__.length}".format(a=Test())
    print "{a[0]}".format(a=Getitem())
    print "{a[0][0]}".format(a=[Getitem()])
    print "{a[0][0]}".format(a=[[1]])
    print "{[0][0]}".format(((1, )))
    print "{[0][0]}".format({0: {0: 1}})
    print "{[0][0]}".format(["test"])
    print "{a.ids[3][1]}".format(a=Test())
    print "{a.ids[3][400]}".format(a=Test())
    print "{a.ids[3]['string']}".format(a=Test())
    print "{[0][1]}".format(["a"])
    print "{0.missing.length}".format(ReturnYes())
    print "{1.missing.length}".format(ReturnYes())
    print "{b[0]}".format(a=23)