# Copyright (c) 2003-2010 Sylvain Thenault (thenault@gmail.com).
# Copyright (c) 2003-2010 LOGILAB S.A. (Paris, FRANCE).
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Python code format's checker.

By default try to follow Guido's style guide :

http://www.python.org/doc/essays/styleguide.html

Some parts of the process_token method is based from The Tab Nanny std module.
"""

import re, sys
import tokenize
if not hasattr(tokenize, 'NL'):
    raise ValueError("tokenize.NL doesn't exist -- tokenize module too old")

from logilab.common.textutils import pretty_match
from logilab.astng import nodes

from pylint.interfaces import IRawChecker, IASTNGChecker
from pylint.checkers import BaseRawChecker
from pylint.checkers.misc import guess_encoding, is_ascii

MSGS = {
    'C0301': ('Line too long (%s/%s)',
              'Used when a line is longer than a given number of characters.'),
    'C0302': ('Too many lines in module (%s)', # was W0302
              'Used when a module has too much lines, reducing its readability.'
              ),

    'W0311': ('Bad indentation. Found %s %s, expected %s',
              'Used when an unexpected number of indentation\'s tabulations or '
              'spaces has been found.'),
    'W0312': ('Found indentation with %ss instead of %ss',
              'Used when there are some mixed tabs and spaces in a module.'),
    'W0301': ('Unnecessary semicolon', # was W0106
              'Used when a statement is ended by a semi-colon (";"), which \
              isn\'t necessary (that\'s python, not C ;).'),

    'F0321': ('Format detection error in %r',
              'Used when an unexpected error occurred in bad format detection.'
              'Please report the error if it occurs.'),
    'C0321': ('More than one statement on a single line',
              'Used when more than on statement are found on the same line.'),
    'C0322': ('Operator not preceded by a space\n%s',
              'Used when one of the following operator (!= | <= | == | >= | < '
              '| > | = | \+= | -= | \*= | /= | %) is not preceded by a space.'),
    'C0323': ('Operator not followed by a space\n%s',
              'Used when one of the following operator (!= | <= | == | >= | < '
              '| > | = | \+= | -= | \*= | /= | %) is not followed by a space.'),
    'C0324': ('Comma not followed by a space\n%s',
              'Used when a comma (",") is not followed by a space.'),

    'W0331': ('Use of the <> operator',
              'Used when the deprecated "<>" operator is used instead \
              of "!=".'),
    'W0332': ('Use l as long integer identifier',
              'Used when a lower case "l" is used to mark a long integer. You '
              'should use a upper case "L" since the letter "l" looks too much '
              'like the digit "1"'),
    'W0333': ('Use of the `` operator',
              'Used when the deprecated "``" (backtick) operator is used '
              'instead  of the str() function.'),
    }

# simple quoted string rgx
SQSTRING_RGX = r'"([^"\\]|\\.)*?"'
# simple apostrophed rgx
SASTRING_RGX = r"'([^'\\]|\\.)*?'"
# triple quoted string rgx
TQSTRING_RGX = r'"""([^"]|("(?!"")))*?(""")'
# triple apostrophed string rgx # FIXME english please
TASTRING_RGX = r"'''([^']|('(?!'')))*?(''')"

# finally, the string regular expression
STRING_RGX = re.compile('(%s)|(%s)|(%s)|(%s)' % (TQSTRING_RGX, TASTRING_RGX,
                                                 SQSTRING_RGX, SASTRING_RGX),
                        re.MULTILINE|re.DOTALL)

COMMENT_RGX = re.compile("#.*$", re.M)

OPERATORS = r'!=|<=|==|>=|<|>|=|\+=|-=|\*=|/=|%'

OP_RGX_MATCH_1 = r'[^(]*(?<!\s|\^|<|>|=|\+|-|\*|/|!|%%|&|\|)(%s).*' % OPERATORS
OP_RGX_SEARCH_1 = r'(?<!\s|\^|<|>|=|\+|-|\*|/|!|%%|&|\|)(%s)' % OPERATORS

OP_RGX_MATCH_2 = r'[^(]*(%s)(?!\s|=|>|<).*' % OPERATORS
OP_RGX_SEARCH_2 = r'(%s)(?!\s|=|>)' % OPERATORS

BAD_CONSTRUCT_RGXS = (

    (re.compile(OP_RGX_MATCH_1, re.M),
     re.compile(OP_RGX_SEARCH_1, re.M),
     'C0322'),

    (re.compile(OP_RGX_MATCH_2, re.M),
     re.compile(OP_RGX_SEARCH_2, re.M),
     'C0323'),

    (re.compile(r'.*,[^(\s|\]|}|\))].*', re.M), 
     re.compile(r',[^\s)]', re.M),
     'C0324'),
    )


def get_string_coords(line):
    """return a list of string positions (tuple (start, end)) in the line
    """
    result = []
    for match in re.finditer(STRING_RGX, line):
        result.append( (match.start(), match.end()) )
    return result

def in_coords(match, string_coords):
    """return true if the match is in the string coord"""
    mstart = match.start()
    for start, end in string_coords:
        if mstart >= start and mstart < end:
            return True
    return False

def check_line(line, writer):
    """check a line for a bad construction
    if it founds one, return a message describing the problem
    else return None
    """
    cleanstr = COMMENT_RGX.sub('', STRING_RGX.sub('', line))
    for rgx_match, rgx_search, msg_id in BAD_CONSTRUCT_RGXS:
        if rgx_match.match(cleanstr):
            string_positions = get_string_coords(line)
            for match in re.finditer(rgx_search, line):
                if not in_coords(match, string_positions):
                    return msg_id, pretty_match(match, line.rstrip())
            #writer.add_message('F0321', line=line, args=line)


class FormatChecker(BaseRawChecker):
    """checks for :
    * unauthorized constructions
    * strict indentation
    * line length
    * use of <> instead of !=
    """

    __implements__ = (IRawChecker, IASTNGChecker)

    # configuration section name
    name = 'format'
    # messages
    msgs = MSGS
    # configuration options
    # for available dict keys/values see the optik parser 'add_option' method
    options = (('max-line-length',
                {'default' : 80, 'type' : "int", 'metavar' : '<int>',
                 'help' : 'Maximum number of characters on a single line.'}),
               ('max-module-lines',
                {'default' : 1000, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of lines in a module'}
                ),
               ('indent-string',
                {'default' : '    ', 'type' : "string", 'metavar' : '<string>',
                 'help' : 'String used as indentation unit. This is usually \
"    " (4 spaces) or "\\t" (1 tab).'}),
               )
    def __init__(self, linter=None):
        BaseRawChecker.__init__(self, linter)
        self._lines = None
        self._visited_lines = None

    def process_module(self, stream):
        """extracts encoding from the stream and decodes each line, so that
        international text's length is properly calculated.
        """
        line_reader = stream.readline
        if sys.version_info < (3, 0):
            data = stream.read()
            if not is_ascii(data)[0]:
                encoding = guess_encoding(data)
                if encoding is not None:
                    line_reader = lambda: stream.readline().decode(encoding,
                                                                   'replace')
            del data

        stream.seek(0)
        self.process_tokens(tokenize.generate_tokens(line_reader))

    def new_line(self, tok_type, line, line_num, junk):
        """a new line has been encountered, process it if necessary"""
        if not tok_type in junk:
            self._lines[line_num] = line.split('\n')[0]
        self.check_lines(line, line_num)

    def process_tokens(self, tokens):
        """process tokens and search for :

         _ non strict indentation (i.e. not always using the <indent> parameter as
           indent unit)
         _ too long lines (i.e. longer than <max_chars>)
         _ optionally bad construct (if given, bad_construct must be a compiled
           regular expression).
        """
        indent = tokenize.INDENT
        dedent = tokenize.DEDENT
        newline = tokenize.NEWLINE
        junk = (tokenize.COMMENT, tokenize.NL)
        indents = [0]
        check_equal = 0
        line_num = 0
        previous = None
        self._lines = {}
        self._visited_lines = {}
        for (tok_type, token, start, _, line) in tokens:
            if start[0] != line_num:
                if previous is not None and previous[0] == tokenize.OP and previous[1] == ';':
                    self.add_message('W0301', line=previous[2])
                previous = None
                line_num = start[0]
                self.new_line(tok_type, line, line_num, junk)
            if tok_type not in (indent, dedent, newline) + junk:
                previous = tok_type, token, start[0]

            if tok_type == tokenize.OP:
                if token == '<>':
                    self.add_message('W0331', line=line_num)
            elif tok_type == tokenize.NUMBER:
                if token.endswith('l'):
                    self.add_message('W0332', line=line_num)

            elif tok_type == newline:
                # a program statement, or ENDMARKER, will eventually follow,
                # after some (possibly empty) run of tokens of the form
                #     (NL | COMMENT)* (INDENT | DEDENT+)?
                # If an INDENT appears, setting check_equal is wrong, and will
                # be undone when we see the INDENT.
                check_equal = 1

            elif tok_type == indent:
                check_equal = 0
                self.check_indent_level(token, indents[-1]+1, line_num)
                indents.append(indents[-1]+1)

            elif tok_type == dedent:
                # there's nothing we need to check here!  what's important is
                # that when the run of DEDENTs ends, the indentation of the
                # program statement (or ENDMARKER) that triggered the run is
                # equal to what's left at the top of the indents stack
                check_equal = 1
                if len(indents) > 1:
                    del indents[-1]

            elif check_equal and tok_type not in junk:
                # this is the first "real token" following a NEWLINE, so it
                # must be the first token of the next program statement, or an
                # ENDMARKER; the "line" argument exposes the leading whitespace
                # for this statement; in the case of ENDMARKER, line is an empty
                # string, so will properly match the empty string with which the
                # "indents" stack was seeded
                check_equal = 0
                self.check_indent_level(line, indents[-1], line_num)

        line_num -= 1 # to be ok with "wc -l"
        if line_num > self.config.max_module_lines:
            self.add_message('C0302', args=line_num, line=1)

    def visit_default(self, node):
        """check the node line number and check it if not yet done"""
        if not node.is_statement:
            return
        if not node.root().pure_python:
            return # XXX block visit of child nodes
        prev_sibl = node.previous_sibling()
        if prev_sibl is not None:
            prev_line = prev_sibl.fromlineno
        else:
            prev_line = node.parent.statement().fromlineno
        line = node.fromlineno
        assert line, node
        if prev_line == line and self._visited_lines.get(line) != 2:
            # py2.5 try: except: finally:
            if not (isinstance(node, nodes.TryExcept)
                    and isinstance(node.parent, nodes.TryFinally)
                    and node.fromlineno == node.parent.fromlineno):
                self.add_message('C0321', node=node)
                self._visited_lines[line] = 2
            return
        if line in self._visited_lines:
            return
        try:
            tolineno = node.blockstart_tolineno
        except AttributeError:
            tolineno = node.tolineno
        assert tolineno, node
        lines = []
        for line in xrange(line, tolineno + 1):
            self._visited_lines[line] = 1
            try:
                lines.append(self._lines[line].rstrip())
            except KeyError:
                lines.append('')
        try:
            msg_def = check_line('\n'.join(lines), self)
            if msg_def:
                self.add_message(msg_def[0], node=node, args=msg_def[1])
        except KeyError:
            # FIXME: internal error !
            pass

    def visit_backquote(self, node):
        self.add_message('W0333', node=node)

    def check_lines(self, lines, i):
        """check lines have less than a maximum number of characters
        """
        max_chars = self.config.max_line_length
        for line in lines.splitlines():
            if len(line) > max_chars:
                self.add_message('C0301', line=i, args=(len(line), max_chars))
            i += 1

    def check_indent_level(self, string, expected, line_num):
        """return the indent level of the string
        """
        indent = self.config.indent_string
        if indent == '\\t': # \t is not interpreted in the configuration file
            indent = '\t'
        level = 0
        unit_size = len(indent)
        while string[:unit_size] == indent:
            string = string[unit_size:]
            level += 1
        suppl = ''
        while string and string[0] in ' \t':
            if string[0] != indent[0]:
                if string[0] == '\t':
                    args = ('tab', 'space')
                else:
                    args = ('space', 'tab')
                self.add_message('W0312', args=args, line=line_num)
                return level
            suppl += string[0]
            string = string [1:]
        if level != expected or suppl:
            i_type = 'spaces'
            if indent[0] == '\t':
                i_type = 'tabs'
            self.add_message('W0311', line=line_num,
                             args=(level * unit_size + len(suppl), i_type,
                                   expected * unit_size))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(FormatChecker(linter))
