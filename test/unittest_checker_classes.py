"""Unit tests for the variables checker."""
import unittest
import sys

from astroid import test_utils
from pylint.checkers import classes
from pylint.testutils import CheckerTestCase, Message, set_config

class VariablesCheckerTC(CheckerTestCase):

    CHECKER_CLASS = classes.ClassChecker

    def test_bitbucket_issue_164(self):
        """Issue 164 report a false negative for access-member-before-definition"""
        n1, n2 = test_utils.extract_node("""
        class MyClass1(object):
          def __init__(self):
            self.first += 5 #@
            self.first = 0  #@
        """)
        with self.assertAddsMessages(Message('access-member-before-definition',
                                             node=n1.target, args=('first', n2.lineno))):
            self.walk(n1.root())

    @set_config(exclude_protected=('_meta', '_manager'))
    def test_exclude_protected(self):
        """Test that exclude-protected can be used to
        exclude names from protected-access warning.
        """

        node = test_utils.build_module("""
        class Protected(object):
            '''empty'''
            def __init__(self):
                self._meta = 42
                self._manager = 24
                self._teta = 29
        OBJ = Protected()
        OBJ._meta
        OBJ._manager
        OBJ._teta
        """)
        with self.assertAddsMessages(
                Message('protected-access',
                        node=node.body[-1].value,
                        args='_teta')):
            self.walk(node.root())

    @unittest.skipUnless(sys.version_info[0] == 3,
                         "The test works on Python 3.")
    def test_regression_non_parent_init_called_tracemalloc(self):
        # This used to raise a non-parent-init-called on Pylint 1.3
        # See issue https://bitbucket.org/logilab/pylint/issue/308/
        # for reference.
        node = test_utils.extract_node("""
        from tracemalloc import Sequence
        class _Traces(Sequence):
            def __init__(self, traces): #@
                Sequence.__init__(self)
        """)
        with self.assertNoMessages():
            self.checker.visit_function(node)


if __name__ == '__main__':
    unittest.main()
