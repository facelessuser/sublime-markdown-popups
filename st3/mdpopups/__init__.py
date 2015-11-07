"""
Markdown popup.

A markdown tooltip for SublimeText.

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions
"""
import sublime
import markdown
import traceback
import os
import re
import time
from collections import OrderedDict
from .st_scheme_template import Scheme2CSS
from .st_clean_css import clean_css

BASE_CSS = 'Packages/mdpopups/themes/__base__.css'
DEFAULT_CSS = 'Packages/mdpopups/themes/default.css'
base_css = None


def _log(msg):
    """Log."""

    print('MarkdownPopup: %s' % msg)


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


def _clear_cache():
    """Clear the css cache."""

    global _scheme_cache
    _scheme_cache = OrderedDict()


def _get_scheme_css(view, css):
    """Get css from scheme."""
    scheme = view.settings().get('color_scheme')
    obj = None
    user_css = ''
    if scheme is not None:
        if scheme in _scheme_cache:
            obj, user_css, t = _scheme_cache[scheme]
            delta_time = _get_setting('mdpopups_cache_refresh_time', 30)
            if not isinstance(delta_time, int) or delta_time < 0:
                delta_time = 30
            if time.time() - t >= (delta_time * 60):
                obj = None
                user_css = ''
        if obj is None:
            try:
                obj = Scheme2CSS(scheme)
                limit = _get_setting('mdpopups_cache_limit', 10)
                if limit is None or not isinstance(limit, int) or limit <= 0:
                    limit = 10
                while len(_scheme_cache) >= limit:
                    _scheme_cache.popitem(last=True)
                user_css = obj.apply_template(_get_user_css(view, scheme))
                print('====user====')
                print(user_css)
                _scheme_cache[scheme] = (obj, user_css, time.time())
            except Exception:
                print(traceback.format_exc())
                pass

    try:
        return obj.get_css() + user_css + obj.apply_template(css) if obj is not None else ''
    except Exception:
        print(traceback.format_exc())
        return ''


def _get_user_css(view, scheme):
    """Get user css."""
    css = None
    scheme_map = _get_setting('mdpopups_scheme_map', {})

    if scheme_map:
        if scheme is not None and scheme in scheme_map:
            try:
                css = clean_css(sublime.load_resource(scheme_map[scheme]))
            except Exception:
                pass
    if css is None:
        default_css = _get_setting('mdpopups_default', DEFAULT_CSS)
        try:
            css = clean_css(sublime.load_resource(default_css))
        except Exception:
            css = clean_css(sublime.load_resource(DEFAULT_CSS))
    print(css)
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
                _log(str(traceback.format_exc()))

        return self


def _get_theme(view, css=None):
    """Get the theme."""
    global base_css
    if base_css is None:
        base_css = clean_css(sublime.load_resource(BASE_CSS))
    return base_css + _get_scheme_css(view, clean_css(css) if css else css)


def _create_html(view, content, md=True, css=None, debug=False):
    """Create html from content."""

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
        content = md2html(content)

    if debug:
        _log('=====HTML OUTPUT=====')
        _log(content)

    html = "<style>%s</style>" % (style)
    html += '<div class="content background foreground">%s</div>' % content
    return html


##############################
# Public functions
##############################
def md2html(markup):
    """Convert Markdown to HTML."""

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
            "css_class": "inlinehilite",
            "use_codehilite_settings": False,
            "guess_lang": False
        },
        "markdown.extensions.codehilite": {
            "guess_lang": False
        },
        "mdpopups.mdx.superfences": {
            "uml_flow": False,
            "uml_sequence": False
        }
    }

    return _MdWrapper(
        extensions=extensions,
        extension_configs=configs
    ).convert(markup).replace('&quot;', '"').replace('\n', '')


def clear_cache():
    """Clear cache."""

    _clear_cache()


def hide_popup(view):
    """Hide the popup."""

    view.hide_popup()


def update_popup(view, content, md=True, css=None):
    """Update the popup."""

    debug = _get_setting('mdpopups_debug')
    disabled = _get_setting('mdpopups_disable', False)
    if disabled:
        if debug:
            _log('Popups disabled')
        return

    if not _can_show(view):
        return

    html = _create_html(view, content, md, css, debug)

    view.update_popup(html)


def show_popup(
    view, content, md=True, css=None,
    flags=0, location=-1, max_width=320, max_height=240,
    on_navigate=None, on_hide=None
):
    """Parse the color scheme if needed and show the styled pop-up."""

    debug = _get_setting('mdpopups_debug')
    disabled = _get_setting('mdpopups_disable', False)
    if disabled:
        if debug:
            _log('Popups disabled')
        return

    if not _can_show(view):
        return

    html = _create_html(view, content, md, css, debug)

    view.show_popup(
        html, flags=flags, location=location, max_width=max_width,
        max_height=max_height, on_navigate=on_navigate, on_hide=on_hide
    )
