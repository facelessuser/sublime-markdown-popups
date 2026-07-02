"""Version."""
from __future__ import annotations

_version_info = (5, 1, 3)
__version__ = '.'.join([str(x) for x in _version_info])


def version() -> tuple[int, int, int]:
    """Get the current version."""

    return _version_info
