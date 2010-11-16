"""some pylint test utilities
"""
from glob import glob
from os.path import join, abspath, dirname, basename, exists
from cStringIO import StringIO

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter

PREFIX = abspath(dirname(__file__))

def fix_path():
    import sys
    sys.path.insert(0, PREFIX)

import sys
MSGPREFIXES = ['2.%s_'%i for i in range(5, 2, -1) if i <= sys.version_info[1]]
MSGPREFIXES.append('')

def get_tests_info(prefix, suffix, inputdir='input', msgdir='messages'):
    """get python input examples and output messages"""
    result = []
    for file in glob(join(PREFIX, 'input', prefix + '*' + suffix)):
        infile = basename(file)
        for msgprefix in MSGPREFIXES:
            outfile = join(PREFIX, 'messages',
                           msgprefix + infile.replace(suffix, '.txt'))
            if exists(outfile):
                break
        result.append((infile, outfile))
    return result


TITLE_UNDERLINES = ['', '=', '-', '.']

class TestReporter(BaseReporter):
    """ store plain text messages 
    """
    
    __implements____ = IReporter
    
    def __init__(self):
        self.message_ids = {}
        self.reset()
        
    def reset(self):
        self.out = StringIO()
        self.messages = []
        
    def add_message(self, msg_id, location, msg):
        """manage message of different type and in the context of path """
        fpath, module, object, line = location
        self.message_ids[msg_id] = 1
        if object:
            object = ':%s' % object
        sigle = msg_id[0]
        self.messages.append('%s:%3s%s: %s' % (sigle, line, object, msg))

    def finalize(self):
        self.messages.sort()
        for msg in self.messages:
            print >>self.out, msg
        result = self.out.getvalue()
        self.reset()
        return result
    
    def display_results(self, layout):
        """ignore layouts"""


# # # # #  pyreverse unittest utilities  # # # # # #

from logilab.common.testlib import TestCase
import os
import sys
from os.path import join

from logilab.astng import MANAGER



def _astng_wrapper(func, modname):
    return func(modname)


def _sorted_file(path):
    lines = [line.strip() for line in open(path).readlines()
             if (line.find('squeleton generated by ') == -1 and
                 not line.startswith('__revision__ = "$Id:'))]
    lines = [line for line in lines if line]
    lines.sort()
    return '\n'.join(lines)

def get_project(module, name=None):
    """return a astng project representation
    """
    manager = MANAGER
    # flush cache
    manager._modules_by_name = {}
    return manager.project_from_files([module], _astng_wrapper,
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
