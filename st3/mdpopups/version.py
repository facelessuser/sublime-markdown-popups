"""Version."""

_version_info = (5, 0, 1)
__version__ = '.'.join([str(x) for x in _version_info])


def version():
    """Get the current version."""

    return _version_info
