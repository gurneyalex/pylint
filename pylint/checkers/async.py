# Copyright (c) 2003-2015 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
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
"""Checker for anything related to the async protocol (PEP 492)."""

import astroid
from astroid import exceptions

from pylint import checkers
from pylint.checkers import utils as checker_utils
from pylint import interfaces
from pylint import utils


class AsyncChecker(checkers.BaseChecker):
    __implements__ = interfaces.IAstroidChecker
    name = 'async'
    msgs = {
        'E1700': ('Yield inside async function',
                  'yield-inside-async-function',
                  'Used when an `yield` or `yield from` statement is '
                  'found inside an async function.',
                  {'minversion': (3, 5)}),
        'E1701': ("Async context manager '%s' doesn't implement __aenter__ and __aexit__.",
                  'not-async-context-manager',
                  'Used when an async context manager is used with an object '
                  'that does not implement the async context management protocol.',
                  {'minversion': (3, 5)}),
    }

    def open(self):
        self._ignore_mixin_members = utils.get_global_option(self, 'ignore-mixin-members')

    @checker_utils.check_messages('yield-inside-async-function')
    def visit_asyncfunctiondef(self, node):
        for child in node.nodes_of_class(astroid.Yield):
            if child.scope() is node:
                self.add_message('yield-inside-async-function', node=child)

    @checker_utils.check_messages('not-async-context-manager')
    def visit_asyncwith(self, node):
        for ctx_mgr, _ in node.items:
            infered = utils.safe_infer(ctx_mgr)
            if infered is None or infered is astroid.YES:
                continue

            if isinstance(infered, astroid.Instance):
                try:
                    infered.getattr('__aenter__')
                    infered.getattr('__aexit__')
                except exceptions.NotFoundError:
                    if isinstance(infered, astroid.Instance):
                        # If we do not know the bases of this class,
                        # just skip it.
                        if not utils.has_known_bases(infered):
                            continue
                        # Just ignore mixin classes.
                        if self._ignore_mixin_members:
                            if infered.name[-5:].lower() == 'mixin':
                                continue
                else:
                    continue

            self.add_message('not-async-context-manager',
                             node=node, args=(infered.name, ))


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(AsyncChecker(linter))
