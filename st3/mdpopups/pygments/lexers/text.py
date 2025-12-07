"""
    pygments.lexers.text
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for non-source code file types.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

# ruff: noqa: F401
from ..lexers.configs import ApacheConfLexer, NginxConfLexer, \
    SquidConfLexer, LighttpdConfLexer, IniLexer, RegeditLexer, PropertiesLexer, \
    UnixConfigLexer
from ..lexers.console import PyPyLogLexer
from ..lexers.textedit import VimLexer
from ..lexers.markup import BBCodeLexer, MoinWikiLexer, RstLexer, \
    TexLexer, GroffLexer
from ..lexers.installers import DebianControlLexer, DebianSourcesLexer, SourcesListLexer
from ..lexers.make import MakefileLexer, BaseMakefileLexer, CMakeLexer
from ..lexers.haxe import HxmlLexer
from ..lexers.sgf import SmartGameFormatLexer
from ..lexers.diff import DiffLexer, DarcsPatchLexer
from ..lexers.data import YamlLexer
from ..lexers.textfmts import IrcLogsLexer, GettextLexer, HttpLexer

__all__ = []
