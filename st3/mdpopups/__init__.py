# -*- coding: utf-8 -*-
"""
Markdown popup.

A markdown tooltip for SublimeText.

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions
"""
import sublime
import markdown
import traceback
import time
from . import colorbox
from collections import OrderedDict
from .st_scheme_template import Scheme2CSS
from .st_clean_css import clean_css
from .st_pygments_highlight import syntax_hl as pyg_syntax_hl
from .st_code_highlight import SublimeHighlight
import re

version_info = (1, 3, 4)
__version__ = '.'.join([str(x) for x in version_info])

BASE_CSS = 'Packages/mdpopups/css/base.css'
DEFAULT_CSS = 'Packages/mdpopups/css/default.css'
DEFAULT_USER_CSS = 'Packages/User/mdpopups.css'
base_css = None
IDK = '''
<style>html {background-color: #333; color: red}</style>
<div><p>¯\_(ツ)_/¯'</p></div>
'''
RE_BAD_ENTITIES = re.compile(r'(&(?!amp;|lt;|gt;|nbsp;)(?:\w+;|#\d+;))')


def _log(msg):
    """Log."""

    print('MarkdownPopup: %s' % str(msg))


def _debug(msg):
    """Debug log."""

    if _get_setting('mdpopups.debug', False):
        _log(msg)


def _get_setting(name, default=None):
    """Get the Sublime setting."""

    return sublime.load_settings('Preferences.sublime-settings').get(name, default)


def _can_show(view):
    """
    Check if popup can be shown.

    I have seen Sublime can sometimes crash if trying
    to do a popup off screen.  Normally it should just not show,
    but sometimes it can crash.  We will check if popup
    can/should be attempted.
    """

    can_show = True
    sel = view.sel()
    if len(sel) >= 1:
        region = view.visible_region()
        if region.begin() > sel[0].b or region.end() < sel[0].b:
            can_show = False
    else:
        can_show = False

    return can_show

##############################
# Theme/Scheme cache management
##############################
_scheme_cache = OrderedDict()
_highlighter_cache = OrderedDict()


def _clear_cache():
    """Clear the css cache."""

    global _scheme_cache
    global _highlighter_cache
    _scheme_cache = OrderedDict()
    _highlighter_cache = OrderedDict()


def _is_cache_expired(cache_time):
    """Check if the cache entry is expired."""

    delta_time = _get_setting('mdpopups.cache_refresh_time', 30)
    if not isinstance(delta_time, int) or delta_time < 0:
        delta_time = 30
    return delta_time == 0 or (time.time() - cache_time) >= (delta_time * 60)


def _prune_cache():
    """Prune older items in cache (related to when they were inserted)."""

    limit = _get_setting('mdpopups.cache_limit', 10)
    if limit is None or not isinstance(limit, int) or limit <= 0:
        limit = 10
    while len(_scheme_cache) >= limit:
        _scheme_cache.popitem(last=True)
    while len(_highlighter_cache) >= limit:
        _highlighter_cache.popitem(last=True)


def _get_sublime_highlighter(view):
    """Get the SublimeHighlighter."""

    scheme = view.settings().get('color_scheme')
    obj = None
    if scheme is not None:
        if scheme in _highlighter_cache:
            obj, t = _highlighter_cache[scheme]
            if _is_cache_expired(t):
                obj = None
        if obj is None:
            try:
                obj = SublimeHighlight(scheme)
                _prune_cache()
                _highlighter_cache[scheme] = (obj, time.time())
            except Exception:
                _log('Failed to get Sublime highlighter object!')
                _debug(traceback.format_exc())
                pass
    return obj


def _get_scheme(view):
    """Get the scheme object and user CSS."""

    scheme = view.settings().get('color_scheme')
    settings = sublime.load_settings("Preferences.sublime-settings")
    obj = None
    user_css = ''
    if scheme is not None:
        if scheme in _scheme_cache:
            obj, user_css, t = _scheme_cache[scheme]
            # Check if cache expired or user changed pygments setting.
            if (
                _is_cache_expired(t) or
                obj.variables.get('use_pygments', True) != (not settings.get('mdpopups.use_sublime_highlighter', False))
            ):
                obj = None
                user_css = ''
        if obj is None:
            try:
                obj = Scheme2CSS(scheme)
                _prune_cache()
                user_css = obj.apply_template(_get_user_css())
                _scheme_cache[scheme] = (obj, user_css, time.time())
            except Exception:
                _log('Failed to convert/retrieve scheme to CSS!')
                _debug(traceback.format_exc())
                pass
    return obj, user_css


def _get_scheme_css(view, css):
    """
    Get css from scheme.

    Retrieve scheme if in cache, or compile CSS
    if not in cache or entry is expired in cache.
    """

    obj, user_css = _get_scheme(view)

    try:
        return obj.get_css() + obj.apply_template(css) + user_css if obj is not None else ''
    except Exception:
        _log('Failed to retrieve scheme CSS!')
        _debug(traceback.format_exc())
        return ''


def _get_user_css():
    """Get user css."""
    css = None

    user_css = _get_setting('mdpopups.user_css', DEFAULT_USER_CSS)
    try:
        css = clean_css(sublime.load_resource(user_css))
    except Exception:
        css = clean_css(sublime.load_resource(DEFAULT_CSS))
    return css if css else ''


##############################
# Markdown parsing
##############################
class _MdWrapper(markdown.Markdown):
    """
    Wrapper around Python Markdown's class.

    This allows us to gracefully continue when a module doesn't load.
    """

    Meta = {}

    def __init__(self, *args, **kwargs):
        """Call original init."""

        super(_MdWrapper, self).__init__(*args, **kwargs)

    def registerExtensions(self, extensions, configs):  # noqa
        """
        Register extensions with this instance of Markdown.

        Keyword arguments:

        * extensions: A list of extensions, which can either
           be strings or objects.  See the docstring on Markdown.
        * configs: A dictionary mapping module names to config options.

        """

        from markdown import util
        from markdown.extensions import Extension

        for ext in extensions:
            try:
                if isinstance(ext, util.string_type):
                    ext = self.build_extension(ext, configs.get(ext, {}))
                if isinstance(ext, Extension):
                    ext.extendMarkdown(self, globals())
                elif ext is not None:
                    raise TypeError(
                        'Extension "%s.%s" must be of type: "markdown.Extension"'
                        % (ext.__class__.__module__, ext.__class__.__name__)
                    )
            except Exception:
                # We want to gracefully continue even if an extension fails.
                _log('Failed to load markdown module!')
                _debug(traceback.format_exc())

        return self


def _get_theme(view, css=None):
    """Get the theme."""
    global base_css
    if base_css is None:
        base_css = clean_css(sublime.load_resource(BASE_CSS))
    return base_css + _get_scheme_css(view, clean_css(css) if css else css)


def _remove_entities(text):
    """Remove unsupported HTML entities."""

    import html.parser
    html = html.parser.HTMLParser()

    def repl(m):
        """Replace entites except &, <, >, and nbsp."""
        return html.unescape(m.group(1))

    return RE_BAD_ENTITIES.sub(repl, text)


def _create_html(view, content, md=True, css=None, debug=False):
    """Create html from content."""

    debug = _get_setting('mdpopups.debug', False)
    if debug:
        _log('=====Content=====')
        _log(content)

    if css is None or not isinstance(css, str):
        css = ''

    style = _get_theme(view, css)

    if debug:
        _log('=====CSS=====')
        _log(style)

    if md:
        content = md2html(view, content)

    if debug:
        _log('=====HTML OUTPUT=====')
        _log(content)

    html = "<style>%s</style>" % (style)
    html += _remove_entities(content)
    return html


##############################
# Public functions
##############################
def version():
    """Get the current version."""

    return version_info


def md2html(view, markup):
    """Convert Markdown to HTML."""

    if _get_setting('mdpopups.use_sublime_highlighter'):
        sublime_hl = (True, _get_sublime_highlighter(view))
    else:
        sublime_hl = (False, None)

    extensions = [
        "markdown.extensions.attr_list",
        "markdown.extensions.codehilite",
        "mdpopups.mdx.superfences",
        "mdpopups.mdx.betterem",
        "mdpopups.mdx.magiclink",
        "mdpopups.mdx.inlinehilite",
        "markdown.extensions.nl2br",
        "markdown.extensions.admonition",
        "markdown.extensions.def_list"
    ]

    configs = {
        "mdpopups.mdx.inlinehilite": {
            "style_plain_text": True,
            "css_class": "inline-highlight",
            "use_codehilite_settings": False,
            "guess_lang": False,
            "sublime_hl": sublime_hl
        },
        "markdown.extensions.codehilite": {
            "guess_lang": False,
            "css_class": "highlight"
        },
        "mdpopups.mdx.superfences": {
            "uml_flow": False,
            "uml_sequence": False,
            "sublime_hl": sublime_hl
        }
    }

    return _MdWrapper(
        extensions=extensions,
        extension_configs=configs
    ).convert(markup).replace('&quot;', '"').replace('\n', '')


def color_box(
    colors, border="#000000ff", border2=None, height=32, width=32,
    border_size=1, check_size=4, max_colors=5, alpha=False, border_map=0xF
):
    """Color box."""

    return colorbox.color_box(
        colors, border, border2, height, width,
        border_size, check_size, max_colors, alpha, border_map
    )


def syntax_highlight(view, src, language=None, inline=False):
    """Syntax highlighting for code."""

    try:
        if _get_setting('mdpopups.use_sublime_highlighter'):
            highlighter = _get_sublime_highlighter(view)
            code = highlighter.syntax_highlight(src, language, inline=inline)
        else:
            code = pyg_syntax_hl(src, language, inline=inline)
    except Exception:
        code = src
        _log('Failed to highlight code!')
        _debug(traceback.format_exc())

    return code


def clear_cache():
    """Clear cache."""

    _clear_cache()


def hide_popup(view):
    """Hide the popup."""

    view.hide_popup()


def update_popup(view, content, md=True, css=None):
    """Update the popup."""

    disabled = _get_setting('mdpopups.disable', False)
    if disabled:
        _debug('Popups disabled')
        return

    if not _can_show(view):
        return

    try:
        html = _create_html(view, content, md, css)
    except Exception:
        _log(traceback.format_exc())
        html = IDK

    view.update_popup(html)


def show_popup(
    view, content, md=True, css=None,
    flags=0, location=-1, max_width=320, max_height=240,
    on_navigate=None, on_hide=None
):
    """Parse the color scheme if needed and show the styled pop-up."""

    disabled = _get_setting('mdpopups.disable', False)
    if disabled:
        _debug('Popups disabled')
        return

    if not _can_show(view):
        return

    try:
        html = _create_html(view, content, md, css)
    except Exception:
        _log(traceback.format_exc())
        html = IDK

    view.show_popup(
        html, flags=flags, location=location, max_width=max_width,
        max_height=max_height, on_navigate=on_navigate, on_hide=on_hide
    )
