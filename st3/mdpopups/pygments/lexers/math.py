# -*- coding: utf-8 -*-
"""
    pygments.lexers.math
    ~~~~~~~~~~~~~~~~~~~~

    Just export lexers that were contained in this module.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from .python import NumPyLexer
from .matlab import MatlabLexer, MatlabSessionLexer, \
    OctaveLexer, ScilabLexer
from .julia import JuliaLexer, JuliaConsoleLexer
from .r import RConsoleLexer, SLexer, RdLexer
from .modeling import BugsLexer, JagsLexer, StanLexer
from .idl import IDLLexer
from .algebra import MuPADLexer

__all__ = []
