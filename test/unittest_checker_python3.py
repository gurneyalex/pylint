# Copyright 2014 Google Inc.
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Tests for the python3 checkers."""
from __future__ import absolute_import

import sys
import unittest

from astroid import test_utils

from pylint import testutils
from pylint.checkers import python3 as checker


def python2_only(test):
    """Decorator for any tests that will fail under Python 3."""
    return unittest.skipIf(sys.version_info[0] > 2, 'Python 2 only')(test)


class Python3CheckerTest(testutils.CheckerTestCase):

    CHECKER_CLASS = checker.Python3Checker

    def check_bad_builtin(self, builtin_name):
        node = test_utils.extract_node(builtin_name + '  #@')
        message = builtin_name.lower() + '-builtin'
        with self.assertAddsMessages(testutils.Message(message, node=node)):
            self.checker.visit_name(node)

    @python2_only
    def test_apply_builtin(self):
        self.check_bad_builtin('apply')

    @python2_only
    def test_buffer_builtin(self):
        self.check_bad_builtin('buffer')

    @python2_only
    def test_cmp_builtin(self):
        self.check_bad_builtin('cmp')

    @python2_only
    def test_coerce_builtin(self):
        self.check_bad_builtin('coerce')

    @python2_only
    def test_execfile_builtin(self):
        self.check_bad_builtin('execfile')

    @python2_only
    def test_file_builtin(self):
        self.check_bad_builtin('file')

    @python2_only
    def test_long_builtin(self):
        self.check_bad_builtin('long')

    @python2_only
    def test_raw_input_builtin(self):
        self.check_bad_builtin('raw_input')

    @python2_only
    def test_reduce_builtin(self):
        self.check_bad_builtin('reduce')

    @python2_only
    def test_StandardError_builtin(self):
        self.check_bad_builtin('StandardError')

    @python2_only
    def test_unicode_builtin(self):
        self.check_bad_builtin('unicode')

    @python2_only
    def test_xrange_builtin(self):
        self.check_bad_builtin('xrange')

    def test_delslice_method(self):
        node = test_utils.extract_node("""
            class Foo(object):
                def __delslice__(self, i, j):  #@
                    pass""")
        message = testutils.Message('delslice-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_function(node)

    def test_getslice_method(self):
        node = test_utils.extract_node("""
            class Foo(object):
                def __getslice__(self, i, j):  #@
                    pass""")
        message = testutils.Message('getslice-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_function(node)

    def test_setslice_method(self):
        node = test_utils.extract_node("""
            class Foo(object):
                def __setslice__(self, i, j, value):  #@
                    pass""")
        message = testutils.Message('setslice-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_function(node)

    def test_coerce_method(self):
        node = test_utils.extract_node("""
            class Foo(object):
                def __coerce__(self, other):  #@
                    pass""")
        message = testutils.Message('coerce-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_function(node)


if __name__ == '__main__':
    unittest.main()
