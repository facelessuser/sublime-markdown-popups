"""Version."""

_version_info = (3, 7, 2)
__version__ = '.'.join([str(x) for x in _version_info])


def version():
    """Get the current version."""

    return _version_info
