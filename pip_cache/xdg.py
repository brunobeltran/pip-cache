""" Functions to handle XDG spec compliance. """
from .externals import six
import os
import sys
def get_home():
    """Find user's home directory if possible.
    Otherwise, returns None.

    :see:
        http://mail.python.org/pipermail/python-list/2005-February/325395.html
    """
    try:
        if six.PY2 and sys.platform == 'win32':
            path = os.path.expanduser(b"~").decode(sys.getfilesystemencoding())
        else:
            path = os.path.expanduser("~")
    except ImportError:
        # This happens on Google App Engine (pwd module is not present).
        pass
    else:
        if os.path.isdir(path):
            return path
    for evar in ('HOME', 'USERPROFILE', 'TMP'):
        path = os.environ.get(evar)
        if path is not None and os.path.isdir(path):
            return path
    return None

def get_xdg_config_dir():
    """
    Returns the XDG configuration directory, according to the `XDG
    base directory spec
    <http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
    """
    path = os.environ.get('XDG_CONFIG_HOME')
    if path is None:
        path = get_home()
        if path is not None:
            path = os.path.join(path, '.config')
    return path

def get_xdg_cache_dir():
    """
    Returns the XDG cache directory, according to the `XDG
    base directory spec
    <http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
    """
    path = os.environ.get('XDG_CACHE_HOME')
    if path is None:
        path = get_home()
        if path is not None:
            path = os.path.join(path, '.cache')
    return path

def get_xdg_data_dir():
    """
    Returns the XDG data directory, according to the `XDG
    base directory spec
    <http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
    """
    path = os.environ.get('XDG_DATA_HOME')
    if path is None:
        path = get_home()
        if path is not None:
            path = os.path.join(os.path.join(path, '.local'), 'share')
    return path

