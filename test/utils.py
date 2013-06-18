"""some pylint test utilities
"""

import os
import sys
from os.path import join, dirname, abspath
import codecs

from logilab.common.testlib import TestCase
from astroid import MANAGER


def _astroid_wrapper(func, modname):
    return func(modname)


def _sorted_file(path):
    # we don't care about the actual encoding, but python3 forces us to pick one
    lines = [line.strip() for line in codecs.open(path, encoding='latin1').readlines()
             if (line.find('squeleton generated by ') == -1 and
                 not line.startswith('__revision__ = "$Id:'))]
    lines = [line for line in lines if line]
    lines.sort()
    return '\n'.join(lines)

def get_project(module, name=None):
    """return a astroid project representation
    """
    manager = MANAGER
    # flush cache
    manager._modules_by_name = {}
    return manager.project_from_files([module], _astroid_wrapper,
                                      project_name=name)

DEFAULTS = {'all_ancestors': None, 'show_associated': None,
            'module_names': None,
            'output_format': 'dot', 'diadefs_file': None, 'quiet': 0,
            'show_ancestors': None, 'classes': (), 'all_associated': None,
            'mode': 'PUB_ONLY', 'show_builtin': False, 'only_classnames': False}

class Config(object):
    """config object for tests"""
    def __init__(self):
        for attr, value in DEFAULTS.items():
            setattr(self, attr, value)

class FileTC(TestCase):
    """base test case for testing file output"""

    generated_files = ()

    def setUp(self):
        self.expected_files = [join(dirname(abspath(__file__)), 'data', file)
                               for file in self.generated_files]

    def tearDown(self):
        for fname in self.generated_files:
            try:
                os.remove(fname)
            except:
                continue

    def _test_same_file(self, index):
        generated_file = self.generated_files[index]
        expected_file = self.expected_files[index]
        generated = _sorted_file(generated_file)
        expected = _sorted_file(expected_file)

        from difflib import unified_diff
        files = "\n *** expected : %s, generated : %s \n"  % (
            expected_file, generated_file)
        self.assertEqual(expected, generated, '%s%s' % (
            files, '\n'.join(line for line in unified_diff(
            expected.splitlines(), generated.splitlines() ))) )
        os.remove(generated_file)


def build_file_case(filetc):
    for i in range(len(filetc.generated_files)):
        setattr(filetc, 'test_same_file_%s' %i,
                lambda self, index=i: self._test_same_file(index))
