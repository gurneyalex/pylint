# Copyright 2014 Michal Nowikowski.
#
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
"""Unittest for the spelling checker."""
import unittest
import tokenize
import io
from astroid import test_utils

from pylint.checkers import spelling

from pylint.testutils import CheckerTestCase, Message, set_config

# try to create enchant dictionary
try:
    import enchant
except ImportError:
    enchant = None

spell_dict = None
if enchant is not None:
    try:
        enchant.Dict("en_US")
        spell_dict = "en_US"
    except enchant.DictNotFoundError:
        pass


def tokenize_str(code):
    return list(tokenize.generate_tokens(io.StringIO(code).readline))


class SpellingCheckerTest(CheckerTestCase):
    CHECKER_CLASS = spelling.SpellingChecker

    @unittest.skipIf(spell_dict is None,
                     "missing python-enchant package or missing spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_coment(self):
        with self.assertAddsMessages(
            Message('wrong-spelling-in-comment', line=1,
                    args=(u'coment', u'# bad coment', '      ^^^^^^', u"comet' or 'comment' or 'cement' or 'comest"))):
            self.checker.process_tokens(tokenize_str(u"# bad coment"))

    @unittest.skipIf(spell_dict is None,
                     "missing python-enchant package or missing spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_docstring(self):
        stmt = test_utils.extract_node(u'def fff():\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'bad coment', '    ^^^^^^', "comet' or 'comment' or 'cement' or 'comest"))):
            self.checker.visit_function(stmt)

        stmt = test_utils.extract_node(u'class Abc(object):\n   """bad comenta"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('comenta', 'bad comenta', '    ^^^^^^', "comet' or 'comment' or 'cement' or 'comest"))):
            self.checker.visit_class(stmt)


if __name__ == '__main__':
    unittest.main()
