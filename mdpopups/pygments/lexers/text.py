# -*- coding: utf-8 -*-
"""
    pygments.lexers.text
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for non-source code file types.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from .configs import ApacheConfLexer, NginxConfLexer, \
    SquidConfLexer, LighttpdConfLexer, IniLexer, RegeditLexer, PropertiesLexer
from .console import PyPyLogLexer
from .textedit import VimLexer
from .markup import BBCodeLexer, MoinWikiLexer, RstLexer, \
    TexLexer, GroffLexer
from .installers import DebianControlLexer, SourcesListLexer
from .make import MakefileLexer, BaseMakefileLexer, CMakeLexer
from .haxe import HxmlLexer
from .diff import DiffLexer, DarcsPatchLexer
from .data import YamlLexer
from .textfmts import IrcLogsLexer, GettextLexer, HttpLexer

__all__ = []
