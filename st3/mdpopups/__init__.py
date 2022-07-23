# -*- coding: utf-8 -*-
"""
Markdown popup.

Markdown tooltips and phantoms for SublimeText.

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions
"""
import sublime
import sublime_api
from . import markdown
from . import jinja2
import traceback
import time
import codecs
import html
import html.parser
import urllib
import functools
import base64
from . import version as ver
from . import colorbox
from collections import OrderedDict
from .st_scheme_template import SchemeTemplate, POPUP, PHANTOM, SHEET
from .st_clean_css import clean_css
from .st_pygments_highlight import syntax_hl as pyg_syntax_hl
from .st_code_highlight import SublimeHighlight
from .st_mapping import lang_map
from . import imagetint
import re
import os
from . import frontmatter
try:
    import bs4
except Exception:
    bs4 = None

HTML_SHEET_SUPPORT = int(sublime.version()) >= 4074

LOCATION = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSS_PATH = os.path.join(LOCATION, 'css', 'default.css')

DEFAULT_CSS = 'Packages/mdpopups/mdpopups_css/default.css'
OLD_DEFAULT_CSS = 'Packages/mdpopups/css/default.css'
DEFAULT_USER_CSS = 'Packages/User/mdpopups.css'
IDK = '''
<style>html {background-color: #333; color: red}</style>
<div><p>¯\\_(ツ)_/¯</p></div>
<div><p>
MdPopups failed to create<br>
the popup/phantom!<br><br>
Check the console to see if<br>
there are helpful errors.</p></div>
'''
HL_SETTING = 'mdpopups.use_sublime_highlighter'
STYLE_SETTING = 'mdpopups.default_style'
RE_BAD_ENTITIES = re.compile(r'(&(?!amp;|lt;|gt;|nbsp;)(?:\w+;|#\d+;))')

NODEBUG = 0
ERROR = 1
WARNING = 2
INFO = 3


def _log(msg):
    """Log."""

    print('mdpopups: {}'.format(str(msg)))


def _debug(msg, level):
    """Debug log."""

    if int(_get_setting('mdpopups.debug', NODEBUG)) >= level:
        _log(msg)


def _get_setting(name, default=None):
    """Get the Sublime setting."""

    return sublime.load_settings('Preferences.sublime-settings').get(name, default)


def _can_show(view, location=-1):
    """
    Check if popup can be shown.

    I have seen Sublime can sometimes crash if trying
    to do a popup off screen.  Normally it should just not show,
    but sometimes it can crash.  We will check if popup
    can/should be attempted.
    """

    can_show = True
    sel = view.sel()
    if location >= 0:
        region = view.visible_region()
        if region.begin() > location or region.end() < location:
            can_show = False
    elif len(sel) >= 1:
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
    """Clear the CSS cache."""

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
    """Get the `SublimeHighlighter` object."""

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
                _debug(traceback.format_exc(), ERROR)
                pass
    return obj


def _get_scheme(scheme):
    """Get the scheme object and user CSS."""

    settings = sublime.load_settings("Preferences.sublime-settings")
    obj = None
    user_css = ''
    default_css = ''
    if scheme is not None:
        if scheme in _scheme_cache:
            obj, user_css, default_css, t = _scheme_cache[scheme]
            # Check if cache expired or user changed Pygments setting.
            if (
                _is_cache_expired(t) or
                obj.use_pygments != (not settings.get(HL_SETTING, True)) or
                obj.default_style != settings.get(STYLE_SETTING, True)
            ):
                obj = None
                user_css = ''
                default_css = ''
        if obj is None:
            try:
                obj = SchemeTemplate(scheme)
                _prune_cache()
                user_css = _get_user_css()
                default_css = _get_default_css()
                _scheme_cache[scheme] = (obj, user_css, default_css, time.time())
            except Exception:
                _log('Failed to convert/retrieve scheme to CSS!')
                _debug(traceback.format_exc(), ERROR)
    return obj, user_css, default_css


def _get_default_css():
    """Get default CSS."""

    css = ''
    try:
        with codecs.open(DEFAULT_CSS_PATH, encoding='utf-8') as f:
            css = clean_css(f.read())
    except Exception:
        pass

    return css


def _get_user_css():
    """Get user CSS."""

    css = None

    user_css = _get_setting('mdpopups.user_css', DEFAULT_USER_CSS)
    if user_css == OLD_DEFAULT_CSS:
        user_css = DEFAULT_CSS
    if user_css == DEFAULT_CSS:
        css = _get_default_css()
    else:
        try:
            css = clean_css(sublime.load_resource(user_css))
        except Exception:
            pass
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
        """Call original initialization."""

        if 'allow_code_wrap' in kwargs:
            self.sublime_wrap = kwargs['allow_code_wrap']
            del kwargs['allow_code_wrap']
        if 'language_map' in kwargs:
            self.plugin_map = kwargs['language_map']
            del kwargs['language_map']
        if 'sublime_hl' in kwargs:
            self.sublime_hl = kwargs['sublime_hl']
            del kwargs['sublime_hl']

        super(_MdWrapper, self).__init__(*args, **kwargs)

    def registerExtensions(self, extensions, configs):  # noqa
        """
        Register extensions with this instance of Markdown.

        Keyword arguments:

        * `extensions`: A list of extensions, which can either
           be strings or objects.  See the docstring on Markdown.
        * `configs`: A dictionary mapping module names to configuration options.

        """

        from .markdown import util
        from .markdown.extensions import Extension

        for ext in extensions:
            try:
                if isinstance(ext, util.string_type):
                    ext = self.build_extension(ext, configs.get(ext, {}))
                if isinstance(ext, Extension):
                    ext._extendMarkdown(self)
                elif ext is not None:
                    raise TypeError(
                        'Extension "{}.{}" must be of type: "markdown.Extension"'.format(
                            ext.__class__.__module__, ext.__class__.__name__
                        )
                    )
            except Exception:
                # We want to gracefully continue even if an extension fails.
                _log('Failed to load markdown module!')
                _debug(traceback.format_exc(), ERROR)

        return self


def _get_theme(view, css=None, css_type=POPUP, template_vars=None):
    """Get the theme."""

    obj, user_css, default_css = _get_scheme(view.settings().get('color_scheme'))
    try:
        return obj.apply_template(
            view,
            default_css + '\n' +
            ((clean_css(css) + '\n') if css else '') +
            user_css,
            css_type,
            template_vars
        ) if obj is not None else ''
    except Exception:
        _log('Failed to retrieve scheme CSS!')
        _debug(traceback.format_exc(), ERROR)
        return ''


def _remove_entities(text):
    """Remove unsupported HTML entities."""

    p = html.parser.HTMLParser()

    def repl(m):
        """Replace entities except &, <, >, and `nbsp`."""
        return p.unescape(m.group(1))

    return RE_BAD_ENTITIES.sub(repl, text)


def _create_html(
    view, content, md=True, css=None, debug=False, css_type=POPUP,
    wrapper_class=None, template_vars=None, template_env_options=None
):
    """Create HTML from content."""

    debug = _get_setting('mdpopups.debug', NODEBUG)

    if css is None or not isinstance(css, str):
        css = ''

    style = _get_theme(view, css, css_type, template_vars)

    if debug:
        _debug('=====CSS=====', INFO)
        _debug(style, INFO)

    if md:
        content = md2html(
            view, content, template_vars=template_vars,
            template_env_options=template_env_options
        )
    else:
        # Strip out frontmatter if found as we don't currently
        # do anything with it when content is just HTML.
        content = _markup_template(frontmatter.get_frontmatter(content)[1], template_vars, template_env_options)

    if debug:
        _debug('=====HTML OUTPUT=====', INFO)
        if bs4:
            soup = bs4.BeautifulSoup(content, "html.parser")
            _debug('\n' + soup.prettify(), INFO)
        else:
            _debug('\n' + content, INFO)

    if wrapper_class:
        wrapper = ('<div class="mdpopups"><div class="{}">'.format(wrapper_class)) + '{}</div></div>'
    else:
        wrapper = '<div class="mdpopups">{}</div>'

    html = "<style>{}</style>".format(style)
    html += _remove_entities(wrapper.format(content))
    return html


def _markup_template(markup, variables, options):
    """Template for markup."""

    if variables:
        if options is None:
            options = {}
        env = jinja2.Environment(**options)
        return env.from_string(markup).render(plugin=variables)
    return markup


##############################
# Public functions
##############################
def version():
    """Get the current version."""

    return ver.version()


def md2html(
    view, markup, template_vars=None, template_env_options=None, **kwargs
):
    """Convert Markdown to HTML."""

    if _get_setting('mdpopups.use_sublime_highlighter', True):
        sublime_hl = (True, _get_sublime_highlighter(view))
    else:
        sublime_hl = (False, None)

    fm, markup = frontmatter.get_frontmatter(markup)

    # We always include these
    extensions = [
        "mdpopups.mdx.highlight",
        "pymdownx.inlinehilite",
        "pymdownx.superfences"
    ]

    configs = {
        "mdpopups.mdx.highlight": {
            "guess_lang": False
        },
        "pymdownx.inlinehilite": {
            "style_plain_text": True
        },
        "pymdownx.superfences": {
            "custom_fences": fm.get('custom_fences', [])
        }
    }

    # Check if plugin is overriding extensions
    md_exts = fm.get('markdown_extensions', None)
    if md_exts is None:
        # No extension override, use defaults
        extensions.extend(
            [
                "markdown.extensions.admonition",
                "markdown.extensions.attr_list",
                "markdown.extensions.def_list",
                "pymdownx.betterem",
                "pymdownx.magiclink",
                "markdown.extensions.md_in_html",
                "markdown.extensions.nl2br"
            ]
        )
    else:
        for ext in md_exts:
            if isinstance(ext, (dict, OrderedDict)):
                k, v = next(iter(ext.items()))
                # We don't allow plugins to overrides the internal color
                if not k.startswith('mdpopups.'):
                    if k == "pymdownx.extrarawhtml":
                        k = 'markdown.extensions.md_in_html'
                        _debug(
                            "Warning: 'pymdownx.extrarawhtml' no longer exists. 'markdown.extensions.md_in_html'"
                            " will be used instead. Plugins should migrate as mdpopups will not redirect in the "
                            "future.",
                            WARNING
                        )
                    extensions.append(k)
                    if v is not None:
                        configs[k] = v
            elif isinstance(ext, str):
                if not ext.startswith('mdpopups.'):
                    if ext == "pymdownx.extrarawhtml":
                        ext = 'markdown.extensions.md_in_html'
                        _debug(
                            "Warning: 'pymdownx.extrarawhtml' no longer exists. 'markdown.extensions.md_in_html'"
                            " will be used instead. Plugins should migrate as mdpopups will not redirect in the"
                            " future.",
                            WARNING
                        )
                    extensions.append(ext)

    return _MdWrapper(
        extensions=extensions,
        extension_configs=configs,
        sublime_hl=sublime_hl,
        allow_code_wrap=fm.get('allow_code_wrap', False),
        language_map=fm.get('language_map', {})
    ).convert(_markup_template(markup, template_vars, template_env_options))


def color_box(
    colors, border="#000000ff", border2=None, height=32, width=32,
    border_size=1, check_size=4, max_colors=5, alpha=False, border_map=0xF
):
    """Color box."""

    return colorbox.color_box(
        colors, border, border2, height, width,
        border_size, check_size, max_colors, alpha, border_map
    )


def color_box_raw(
    colors, border="#000000ff", border2=None, height=32, width=32,
    border_size=1, check_size=4, max_colors=5, alpha=False, border_map=0xF
):
    """Color box raw."""

    return colorbox.color_box_raw(
        colors, border, border2, height, width,
        border_size, check_size, max_colors, alpha, border_map
    )


def tint(img, color, opacity=255, height=None, width=None):
    """Tint the image."""

    if isinstance(img, str):
        try:
            img = sublime.load_binary_resource(img)
        except Exception:
            _log('Could not open binary file!')
            _debug(traceback.format_exc(), ERROR)
            return ''
    return imagetint.tint(img, color, opacity, height, width)


def tint_raw(img, color, opacity=255):
    """Tint the image."""

    if isinstance(img, str):
        try:
            img = sublime.load_binary_resource(img)
        except Exception:
            _log('Could not open binary file!')
            _debug(traceback.format_exc(), ERROR)
            return ''
    return imagetint.tint_raw(img, color, opacity)


def get_language_from_view(view):
    """Guess current language from view."""

    lang = None
    user_map = sublime.load_settings('Preferences.sublime-settings').get('mdpopups.sublime_user_lang_map', {})
    syntax = os.path.splitext(view.settings().get('syntax').replace('Packages/', '', 1))[0]
    keys = set(list(lang_map.keys()) + list(user_map.keys()))
    for key in keys:
        v1 = lang_map.get(key, (tuple(), tuple()))[1]
        v2 = user_map.get(key, (tuple(), tuple()))[1]
        if syntax in (tuple(v2) + v1):
            lang = key
            break
    return lang


def syntax_highlight(view, src, language=None, inline=False, allow_code_wrap=False, language_map=None):
    """Syntax highlighting for code."""

    try:
        if _get_setting('mdpopups.use_sublime_highlighter', True):
            highlighter = _get_sublime_highlighter(view)
            code = highlighter.syntax_highlight(
                src, language, inline=inline, code_wrap=(not inline and allow_code_wrap), plugin_map=language_map
            )
        else:
            code = pyg_syntax_hl(
                src, language, inline=inline, code_wrap=(not inline and allow_code_wrap)
            )
    except Exception:
        code = src
        _log('Failed to highlight code!')
        _debug(traceback.format_exc(), ERROR)

    return code


def tabs2spaces(text, tab_size=4):
    """
    Convert tabs to spaces on tab stops.

    Does not account for char width.
    """

    return text.expandtabs(tab_size)


def scope2style(view, scope, selected=False, explicit_background=False):
    """Convert the scope to a style."""

    style = {
        'color': None,
        'background': None,
        'style': ''
    }
    obj = _get_scheme(view.settings().get('color_scheme'))[0]
    style_obj = obj.guess_style(view, scope, selected, explicit_background)
    style['color'] = style_obj['foreground']
    style['background'] = style_obj['background']
    font = []
    if style_obj['bold']:
        font.append('bold')
    if style_obj['italic']:
        font.append('italic')
    if style_obj['underline']:
        font.append('underline')
    if style_obj['glow']:
        font.append('glow')
    style['style'] = ' '.join(font)

    return style


def clear_cache():
    """Clear cache."""

    _clear_cache()


def hide_popup(view):
    """Hide the popup."""

    view.hide_popup()


def update_popup(
    view, content, md=True, css=None, wrapper_class=None,
    template_vars=None, template_env_options=None, **kwargs
):
    """Update the popup."""

    disabled = _get_setting('mdpopups.disable', False)
    if disabled:
        _debug('Popups disabled', WARNING)
        return

    try:
        html = _create_html(
            view, content, md, css, css_type=POPUP, wrapper_class=wrapper_class,
            template_vars=template_vars, template_env_options=template_env_options
        )
    except Exception:
        _log(traceback.format_exc())
        html = IDK

    view.update_popup(html)


def show_popup(
    view, content, md=True, css=None,
    flags=0, location=-1, max_width=320, max_height=240,
    on_navigate=None, on_hide=None, wrapper_class=None,
    template_vars=None, template_env_options=None, **kwargs
):
    """Parse the color scheme if needed and show the styled pop-up."""

    disabled = _get_setting('mdpopups.disable', False)
    if disabled:
        _debug('Popups disabled', WARNING)
        return

    if not _can_show(view, location):
        return

    try:
        html = _create_html(
            view, content, md, css, css_type=POPUP, wrapper_class=wrapper_class,
            template_vars=template_vars, template_env_options=template_env_options
        )
    except Exception:
        _log(traceback.format_exc())
        html = IDK

    view.show_popup(
        html, flags=flags, location=location, max_width=max_width,
        max_height=max_height, on_navigate=on_navigate, on_hide=on_hide
    )


def is_popup_visible(view):
    """Check if popup is visible."""

    return view.is_popup_visible()


def add_phantom(
    view, key, region, content, layout, md=True,
    css=None, on_navigate=None, wrapper_class=None,
    template_vars=None, template_env_options=None, **kwargs
):
    """Add a phantom and return phantom id."""

    disabled = _get_setting('mdpopups.disable', False)
    if disabled:
        _debug('Phantoms disabled', WARNING)
        return

    try:
        html = _create_html(
            view, content, md, css, css_type=PHANTOM, wrapper_class=wrapper_class,
            template_vars=template_vars, template_env_options=template_env_options
        )
    except Exception:
        _log(traceback.format_exc())
        html = IDK

    return view.add_phantom(key, region, html, layout, on_navigate)


def erase_phantoms(view, key):
    """Erase phantoms."""

    view.erase_phantoms(key)


def erase_phantom_by_id(view, pid):
    """Erase phantom by ID."""

    view.erase_phantom_by_id(pid)


def query_phantom(view, pid):
    """Query phantom."""

    return view.query_phantom(pid)


def query_phantoms(view, pids):
    """Query phantoms."""

    return view.query_phantoms(pids)


if HTML_SHEET_SUPPORT:
    def new_html_sheet(
        window, name, contents, md=True, css=None, flags=0, group=-1,
        wrapper_class=None, template_vars=None, template_env_options=None, **kwargs
    ):
        """Create new HTML sheet."""

        view = window.create_output_panel('mdpopups-dummy', unlisted=True)
        try:
            html = _create_html(
                view, contents, md, css, css_type=SHEET, wrapper_class=wrapper_class,
                template_vars=template_vars, template_env_options=template_env_options
            )
        except Exception:
            _log(traceback.format_exc())
            html = IDK

        return window.new_html_sheet(name, html, flags, group)

    def update_html_sheet(
        sheet, contents, md=True, css=None, wrapper_class=None,
        template_vars=None, template_env_options=None, **kwargs
    ):
        """Update an HTML sheet."""

        window = sheet.window()

        # Probably a transient sheet, just get a window
        if window is None:
            window = sublime.active_window()

        view = window.create_output_panel('mdpopups-dummy', unlisted=True)

        try:
            html = _create_html(
                view, contents, md, css, css_type=SHEET, wrapper_class=wrapper_class,
                template_vars=template_vars, template_env_options=template_env_options
            )
        except Exception:
            _log(traceback.format_exc())
            html = IDK

        sublime_api.html_sheet_set_contents(sheet.id(), html)


class Phantom(sublime.Phantom):
    """A phantom object."""

    def __init__(
        self, region, content, layout, md=True,
        css=None, on_navigate=None, wrapper_class=None,
        template_vars=None, template_env_options=None, **kwargs
    ):
        """Initialize."""

        super().__init__(region, content, layout, on_navigate)
        self.md = md
        self.css = css
        self.wrapper_class = wrapper_class
        self.template_vars = template_vars
        self.template_env_options = template_env_options

    def __eq__(self, rhs):
        """Check if phantoms are equal."""

        # Note that self.id is not considered
        return (
            self.region == rhs.region and self.content == rhs.content and
            self.layout == rhs.layout and self.on_navigate == rhs.on_navigate and
            self.md == rhs.md and self.css == rhs.css and
            self.wrapper_class == rhs.wrapper_class and self.template_vars == rhs.template_vars and
            self.template_env_options == rhs.template_env_options
        )


class PhantomSet(sublime.PhantomSet):
    """Object that allows easy updating of phantoms."""

    def __init__(self, view, key=""):
        """Initialize."""

        super().__init__(view, key)

    def __del__(self):
        """Delete phantoms."""

        for p in self.phantoms:
            erase_phantom_by_id(self.view, p.id)

    def update(self, new_phantoms):
        """Update the list of phantoms that exist in the text buffer with their current location."""

        regions = query_phantoms(self.view, [p.id for p in self.phantoms])
        for i in range(len(regions)):
            self.phantoms[i].region = regions[i]

        count = 0
        for p in new_phantoms:
            if not isinstance(p, Phantom):
                # Convert sublime.Phantom to mdpopups.Phantom
                p = Phantom(
                    p.region, p.content, p.layout,
                    md=False, css=None, on_navigate=p.on_navigate, wrapper_class=None,
                    template_vars=None, template_env_options=None
                )
                new_phantoms[count] = p
            try:
                # Phantom already exists, copy the id from the current one
                idx = self.phantoms.index(p)
                p.id = self.phantoms[idx].id
            except ValueError:
                p.id = add_phantom(
                    self.view,
                    self.key,
                    p.region,
                    p.content,
                    p.layout,
                    p.md,
                    p.css,
                    p.on_navigate,
                    p.wrapper_class,
                    p.template_vars,
                    p.template_env_options
                )
            count += 1

        for p in self.phantoms:
            # if the region is -1, then it's already been deleted, no need to call erase
            if p not in new_phantoms and p.region != sublime.Region(-1):
                erase_phantom_by_id(self.view, p.id)

        self.phantoms = new_phantoms


def format_frontmatter(values):
    """Format values as frontmatter."""

    return frontmatter.dump_frontmatter(values)


RE_TAG_HTML = re.compile(
    r'''(?xus)
    (?:
        (?P<avoid>
            <\s*(?P<script_name>script|style)[^>]*>.*?</\s*(?P=script_name)\s*> |
            (?:(\r?\n?\s*)<!--[\s\S]*?-->(\s*)(?=\r?\n)|<!--[\s\S]*?-->)
        )|
        (?P<open><\s*(?P<tag>img))
        (?P<attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)
        (?P<close>\s*(?:\/?)>)
    )
    '''
)

RE_TAG_LINK_ATTR = re.compile(
    r'''(?xus)
    (?P<attr>
        (?:
            (?P<name>\s+src\s*=\s*)
            (?P<path>"[^"]*"|'[^']*')
        )
    )
    '''
)


def _image_parser(text):
    """Retrieve image source whose attribute `src` URL has scheme 'http' or 'https'."""

    images = {}
    for m in RE_TAG_HTML.finditer(text):
        if m.group('avoid'):
            continue
        start = m.start('attr')
        m2 = RE_TAG_LINK_ATTR.search(m.group('attr'))
        if m2:
            src = m2.group('path')[1:-1]
            src = html.parser.HTMLParser().unescape(src)
            if urllib.parse.urlparse(src).scheme in ("http", "https"):
                s = start + m2.start('path') + 1
                e = start + m2.end('path') - 1
                images.setdefault(src, []).append((s, e))
    return images


class _ImageResolver:
    """
    Keeps track of which images are downloaded, and builds the final html after all of them have been downloaded.

    Note that this entire class is a workaround for not having a scatter-gather function and not having a promise type.
    In an asynchronous world, we would of course use `asyncio.gather`.
    """

    def __init__(self, minihtml, resolver, done_callback, images_to_resolve):
        """The constructor."""
        self.minihtml = minihtml
        self.done_callback = done_callback
        self.images_to_resolve = images_to_resolve
        self.resolved = {}
        for url in self.images_to_resolve.keys():
            resolver(url, functools.partial(self.on_image_resolved, url))

    def on_image_resolved(self, url, data, mime, exception):
        """
        Called by a resolver when an image has been downloaded.

        The `data` is a bytes object.
        The `mime` is the mime-type, e.g. image/png.
        When the resolver function encountered an exception, the exception is passed in via the last
        argument. So its type is Optional[Exception].
        """
        if exception:
            value = (exception, None)
        else:
            value = (base64.b64encode(data).decode("ascii"), mime)
        self.resolved[url] = value
        if len(self.resolved) == len(self.images_to_resolve):
            self.finalize()

    def finalize(self):
        """
        Called when all necessary images have been downloaded.

        This method reconstructs the final html to be presented.

        It invokes the `done_callback` from the `resolve_urls` function in the main thread of Sublime Text.
        """

        def flattened():
            for url, positions in self.images_to_resolve.items():
                for position in positions:
                    yield url, position[0], position[1]

        todo = sorted(flattened(), key=lambda t: (t[1], t[2]))
        chunks = [self.minihtml[:todo[0][1]]]
        for index in range(0, len(todo)):
            next_index = index + 1
            if next_index >= len(todo):
                next_start = len(self.minihtml)
            else:
                next_start = todo[next_index][1]
            data, mime = self.resolved[todo[index][0]]
            current_end = todo[index][2]
            if isinstance(data, Exception):
                # keep the minihtml unchanged
                current_start = todo[index][1]
                chunks.append(self.minihtml[current_start:current_end])
            else:
                # replace the URL with the base64 data
                chunks.append("data:")
                chunks.append(mime)
                chunks.append(";base64,")
                chunks.append(data)
            chunks.append(self.minihtml[current_end:next_start])
        finalhtml = "".join(chunks)
        sublime.set_timeout(lambda: self.done_callback(finalhtml))


@functools.lru_cache(maxsize=8)
def _retrieve(url):
    """
    Actually download the image pointed to by the passed URL.

    The most recently used images (8 at most) are kept in a cache.
    """
    import urllib.request
    with urllib.request.urlopen(url) as response:
        # We provide some basic protection against absurdly large images.
        # 32MB is chosen as an arbitrary upper limit. This can be raised if desired.
        length = response.headers.get("content-length")
        if length is None:
            raise ValueError("missing content-length header")
        length = int(length)
        if length == 0:
            raise ValueError("empty payload")
        elif length >= 32 * 1024 * 1024:
            raise ValueError("refusing to read payloads larger than or equal to 32MB")
        mime = response.headers.get("content-type", "image/png").lower()
        return response.readall(), mime


def blocking_resolver(url, done):
    """A simple URL resolver that will block the caller."""
    exception = None
    payload = None
    mime = None
    try:
        payload, mime = _retrieve(url)
    except Exception as ex:
        exception = ex
    if exception:
        done(None, None, exception)
    elif payload and mime:
        done(payload, mime, None)
    else:
        done(None, None, RuntimeError("failed to retrieve image"))


def ui_thread_resolver(url, done):
    """A URL resolver that runs on the main thread."""
    sublime.set_timeout(lambda: blocking_resolver(url, done))


def worker_thread_resolver(url, done):
    """A URL resolver that runs on the worker ("async") thread of Sublime Text."""
    sublime.set_timeout_async(lambda: blocking_resolver(url, done))


def resolve_images(minihtml, resolver, on_done):
    """
    Download images from the internet.

    Given minihtml containing `<img>` tags with a `src` attribute that points to an image located on the internet,
    download those images and replace the `src` attribute with embedded base64-encoded image data.

    The first argument is minihtml as returned by the `md2html` function.

    The second argument is a callable that shall take two arguments.

    - The first argument is a URL to be downloaded.
    - The second argument is a callable that shall take one argument: An object of type `bytes`: the raw image data.
      The result of downloading the image.

    The third argument is a callable that shall take one argument:

    - A string that is the final minihtml containing embedded base64 encoded images, ready to be presented to a view.

    This function is non-blocking.
    It will invoke the passed-in `done_callback` on the UI thread.
    It returns an opaque object that should be kept alive for as long as the passed-in `done_callback` is not yet
    invoked.
    """
    images = _image_parser(minihtml)
    if images:
        return _ImageResolver(minihtml, resolver, on_done, images)
    else:
        sublime.set_timeout(lambda: on_done(minihtml))
        return None
