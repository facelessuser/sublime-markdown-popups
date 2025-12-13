"""
    pygments.lexers.functional
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Just export lexer classes previously contained in this module.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

# ruff: noqa: F401
from ..lexers.lisp import SchemeLexer, CommonLispLexer, RacketLexer, \
    NewLispLexer, ShenLexer
from ..lexers.haskell import HaskellLexer, LiterateHaskellLexer, \
    KokaLexer
from ..lexers.theorem import CoqLexer
from ..lexers.erlang import ErlangLexer, ErlangShellLexer, \
    ElixirConsoleLexer, ElixirLexer
from ..lexers.ml import SMLLexer, OcamlLexer, OpaLexer

__all__ = []
