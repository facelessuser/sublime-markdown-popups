"""
Sublime Text Scheme template.

Converts scheme to CSS provides templating for
additional so that they can access the colors.

Licensed under MIT
Copyright (c) 2015 - 2020 Isaac Muse <isaacmuse@gmail.com>

----------------------

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions
"""
import sublime
import re
from . import version as ver
from .coloraide import util
from .st_colormod import Color
from . import jinja2
from .pygments.formatters import HtmlFormatter
from collections import OrderedDict
from .st_clean_css import clean_css
import copy
import codecs
import os

LOCATION = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSS_PATH = os.path.join(LOCATION, 'css', 'default.css')

INVALID = -1
POPUP = 0
PHANTOM = 1
SHEET = 2
LUM_MIDPOINT = 127

re_float_trim = re.compile(r'^(?P<keep>\d+)(?P<trash>\.0+|(?P<keep2>\.\d*[1-9])0+)$')
re_valid_custom_scopes = re.compile(r'[a-zA-Z\d]+[a-zA-Z\d._\-]*')
re_missing_semi_colon = re.compile(r'(?<!;) \}')

re_base_colors = re.compile(r'^\s*\.(?:dummy)\s*\{([^}]+)\}', re.MULTILINE)
re_color = re.compile(r'(?<!-)(color\s*:\s*#[A-Fa-z\d]{6})')
re_bgcolor = re.compile(r'(?<!-)(background(?:-color)?\s*:\s*#[A-Fa-z\d]{6})')
re_pygments_selectors = re.compile(r'\.dummy (\.[a-zA-Z\d]+) ')
CODE_BLOCKS = '.mdpopups .highlight, .mdpopups .inline-highlight {{ {}; {}; }}'
OLD_DEFAULT_CSS = 'Packages/mdpopups/css/default.css'
DEFAULT_CSS = 'Packages/mdpopups/mdpopups_css/default.css'


class _Filters:
    """Color filters."""

    @staticmethod
    def colorize(color, deg):
        """Colorize the color with the given hue."""

        if color.is_nan('hsl.hue'):
            return
        color.set('hsl.hue', deg % 360)

    @staticmethod
    def hue(color, deg):
        """Shift the hue."""

        if color.get('hsl.is_nan'):
            return
        h = color.get('hsl.hue')
        h += deg
        h = color.set('hsl.hue', h % 360)

    @staticmethod
    def contrast(color, factor):
        """Adjust contrast."""

        r, g, b = [util.round_half_up(util.clamp(c * 255, 0, 255)) for c in util.no_nan(color.coords())]
        # Algorithm can't handle any thing beyond +/-255 (or a factor from 0 - 2)
        # Convert factor between (-255, 255)
        f = (util.clamp(factor, 0.0, 2.0) - 1.0) * 255.0
        f = (259 * (f + 255)) / (255 * (259 - f))

        # Increase/decrease contrast accordingly.
        r = util.clamp(util.round_half_up((f * (r - 128)) + 128), 0, 255)
        g = util.clamp(util.round_half_up((f * (g - 128)) + 128), 0, 255)
        b = util.clamp(util.round_half_up((f * (b - 128)) + 128), 0, 255)
        color.red = r / 255
        color.green = g / 255
        color.blue = b / 255

    @staticmethod
    def invert(color):
        """Invert the color."""

        r, g, b = [int(util.round_half_up(util.clamp(c * 255, 0, 255))) for c in util.no_nan(color.coords())]
        r ^= 0xFF
        g ^= 0xFF
        b ^= 0xFF
        color.red = r / 255
        color.green = g / 255
        color.blue = b / 255

    @staticmethod
    def saturation(color, factor):
        """Saturate or unsaturate the color by the given factor."""

        s = util.no_nan(color.get('hsl.saturation')) / 100.0
        s = util.clamp(s + factor - 1.0, 0.0, 1.0)
        color.set('hsl.saturation', s * 100)

    @staticmethod
    def grayscale(color):
        """Convert the color with a grayscale filter."""

        luminance = color.luminance()
        color.red = luminance
        color.green = luminance
        color.blue = luminance

    @staticmethod
    def sepia(color):
        """Apply a sepia filter to the color."""

        red, green, blue = util.no_nan(color.coords())
        r = util.clamp((red * .393) + (green * .769) + (blue * .189), 0, 1)
        g = util.clamp((red * .349) + (green * .686) + (blue * .168), 0, 1)
        b = util.clamp((red * .272) + (green * .534) + (blue * .131), 0, 1)
        color.red = r
        color.green = g
        color.blue = b

    @staticmethod
    def _get_overage(c):
        """Get overage."""

        if c < 0.0:
            o = 0.0 + c
            c = 0.0
        elif c > 255.0:
            o = c - 255.0
            c = 255.0
        else:
            o = 0.0
        return o, c

    @staticmethod
    def _distribute_overage(c, o, s):
        """Distribute overage."""

        channels = len(s)
        if channels == 0:
            return c
        parts = o / len(s)
        if "r" in s and "g" in s:
            c = c[0] + parts, c[1] + parts, c[2]
        elif "r" in s and "b" in s:
            c = c[0] + parts, c[1], c[2] + parts
        elif "g" in s and "b" in s:
            c = c[0], c[1] + parts, c[2] + parts
        elif "r" in s:
            c = c[0] + parts, c[1], c[2]
        elif "g" in s:
            c = c[0], c[1] + parts, c[2]
        else:  # "b" in s:
            c = c[0], c[1], c[2] + parts
        return c

    @classmethod
    def brightness(cls, color, factor):
        """
        Adjust the brightness by the given factor.

        Brightness is determined by perceived luminance.
        """

        red, green, blue = [util.round_half_up(util.clamp(c * 255, 0, 255)) for c in util.no_nan(color.coords())]
        channels = ["r", "g", "b"]
        total_lumes = util.clamp(util.clamp(color.luminance(), 0, 1) * 255 + (255.0 * factor) - 255.0, 0.0, 255.0)

        if total_lumes == 255.0:
            # white
            r, g, b = 1, 1, 1
        elif total_lumes == 0.0:
            # black
            r, g, b = 0, 0, 0
        else:
            # Adjust Brightness
            pts = (total_lumes - util.clamp(color.luminance(), 0, 1) * 255)
            slots = set(channels)
            components = [float(red) + pts, float(green) + pts, float(blue) + pts]
            count = 0
            for c in channels:
                overage, components[count] = cls._get_overage(components[count])
                if overage:
                    slots.remove(c)
                    components = list(cls._distribute_overage(components, overage, slots))
                count += 1

            r = util.clamp(util.round_half_up(components[0]), 0, 255) / 255.0
            g = util.clamp(util.round_half_up(components[1]), 0, 255) / 255.0
            b = util.clamp(util.round_half_up(components[2]), 0, 255) / 255.0
        color.red = r
        color.green = g
        color.blue = b


class SchemeTemplate(object):
    """Determine color scheme colors and style for text in a Sublime view buffer."""

    def __init__(self, scheme_file):
        """Initialize."""

        self.scheme_file = scheme_file
        self.css_type = INVALID
        self.variable = {}
        self.view = None
        self.setup()

    def guess_style(self, view, scope, selected=False, explicit_background=False):
        """Guess color."""

        # Remove leading '.' to account for old style CSS
        scope_style = view.style_for_scope(scope.lstrip('.'))
        style = {}
        style['foreground'] = scope_style['foreground']
        style['background'] = scope_style.get('background')
        style['bold'] = scope_style.get('bold', False)
        style['italic'] = scope_style.get('italic', False)
        style['underline'] = scope_style.get('underline', False)
        style['glow'] = scope_style.get('glow', False)

        defaults = view.style()
        if not explicit_background and not style.get('background'):
            style['background'] = defaults.get('background', '#FFFFFF')
        if selected:
            sfg = scope_style.get('selection_foreground', defaults.get('selection_foreground'))
            if sfg != '#00000000':
                style['foreground'] = sfg
            style['background'] = defaults.get('selection', '#0000FF')
        return style

    def get_variables(self):
        """Get variables."""

        is_dark = self.is_dark()
        return {
            "is_dark": is_dark,
            "is_light": not is_dark,
            "sublime_version": int(sublime.version()),
            "mdpopups_version": ver.version(),
            "color_scheme": self.scheme_file,
            "use_pygments": self.use_pygments,
            "default_style": self.default_style
        }

    def get_html_border(self):
        """Get HTML border."""

        return self.get_bg()

    def is_dark(self):
        """Check if scheme is dark."""

        return self.get_lums() <= LUM_MIDPOINT

    def get_lums(self):
        """Get luminance."""

        bg = self.get_bg()
        rgba = Color(bg)
        return rgba.luminance()

    def get_fg(self):
        """Get foreground."""

        return self.view.style().get('foreground', '#000000')

    def get_bg(self):
        """Get background."""

        return self.view.style().get('background', '#FFFFFF')

    def setup(self):
        """Setup the template environment."""

        settings = sublime.load_settings("Preferences.sublime-settings")
        self.use_pygments = not settings.get('mdpopups.use_sublime_highlighter', True)
        self.default_style = settings.get('mdpopups.default_style', True)

        # Create Jinja template
        self.env = jinja2.Environment()
        self.env.filters['css'] = self.retrieve_selector
        self.env.filters['pygments'] = self.pygments
        self.env.filters['foreground'] = self.to_fg
        self.env.filters['background'] = self.to_bg
        self.env.filters['brightness'] = self.brightness
        self.env.filters['colorize'] = self.colorize
        self.env.filters['hue'] = self.hue
        self.env.filters['invert'] = self.invert
        self.env.filters['saturation'] = self.saturation
        self.env.filters['contrast'] = self.contrast
        self.env.filters['grayscale'] = self.grayscale
        self.env.filters['sepia'] = self.sepia
        self.env.filters['fade'] = self.fade
        self.env.filters['getcss'] = self.read_css

    def read_css(self, css):
        """Read the CSS file."""

        try:
            var = copy.copy(self.variables)
            var.update(
                {
                    'is_phantom': self.css_type == PHANTOM,
                    'is_popup': self.css_type == POPUP,
                    'is_sheet': self.css_type == SHEET
                }
            )

            if css == OLD_DEFAULT_CSS:
                css = DEFAULT_CSS

            if css == DEFAULT_CSS:
                css = ''
                try:
                    with codecs.open(DEFAULT_CSS_PATH, encoding='utf-8') as f:
                        css = clean_css(f.read())
                except Exception:
                    pass

                return self.env.from_string(css).render(var=var, plugin=self.plugin_vars)

            return self.env.from_string(
                clean_css(sublime.load_resource(css))
            ).render(var=var, plugin=self.plugin_vars)
        except Exception:
            return ''

    def fade(self, css, factor):
        """
        Apply a fake transparency to color.

        Fake transparency is preformed on top of the background color.
        """
        try:
            parts = [c.strip('; ') for c in css.split(':')]
            if len(parts) == 2 and parts[0] in ('background-color', 'color'):
                rgba = Color(parts[1])
                rgba.alpha = max(min(float(factor), 1.0), 0.0)
                rgba.compose(self.get_bg())
                return '{}: {}; '.format(parts[0], rgba.to_string(hex=True))
        except Exception:
            pass
        return css

    def colorize(self, css, degree):
        """Colorize to the given hue."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.colorize(rgba, degree)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def hue(self, css, degree):
        """Shift hue."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.hue(rgba, degree)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def invert(self, css):
        """Invert color."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.invert(rgba)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def contrast(self, css, factor):
        """Apply contrast filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.contrast(rgba, factor)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def saturation(self, css, factor):
        """Apply saturation filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.saturation(rgba, factor)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def grayscale(self, css):
        """Apply grayscale filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.grayscale(rgba)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def sepia(self, css):
        """Apply sepia filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.sepia(rgba)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def brightness(self, css, factor):
        """Adjust brightness."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = Color(parts[1])
            _Filters.brightness(rgba, factor)
            parts[1] = "{}; ".format(rgba.to_string(hex=True))
            return '{}: {} '.format(parts[0], parts[1])
        return css

    def to_fg(self, css):
        """Rename a CSS key value pair."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] == 'background-color':
            parts[0] = 'color'
            return '{}: {}; '.format(parts[0], parts[1])
        return css

    def to_bg(self, css):
        """Rename a CSS key value pair."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] == 'color':
            parts[0] = 'background-color'
            return '{}: {}; '.format(parts[0], parts[1])
        return css

    def pygments(self, style):
        """Get Pygments style."""

        return get_pygments(style)

    def retrieve_selector(self, selector, key=None, explicit_background=True):
        """Get the CSS key, value pairs for a rule."""

        general = self.view.style()
        fg = general.get('foreground', '#000000')
        bg = general.get('background', '#ffffff')
        scope = self.view.style_for_scope(selector)
        style = []
        if scope.get('bold', False):
            style.append('bold')
        if scope.get('italic', False):
            style.append('italic')
        if scope.get('underline', False):
            style.append('underline')
        if scope.get('glow', False):
            style.append('glow')
        color = scope.get('foreground', fg)
        bgcolor = scope.get('background', (None if explicit_background else bg))

        css = []
        if color and (key is None or key == 'color'):
            css.append('color: {}'.format(color))
        if bgcolor and (key is None or key == 'background-color'):
            css.append('background-color: {}'.format(bgcolor))
        for s in style:
            if "bold" in s and (key is None or key == 'font-weight'):
                css.append('font-weight: bold')
            if "italic" in s and (key is None or key == 'font-style'):
                css.append('font-style: italic')
            if "underline" in s and (key is None or key == 'text-decoration'):
                css.append('text-decoration: underline')
            if "glow" in s and (key is None or key == 'text-shadow'):
                css.append('text-shadow: 0 0 3px currentColor')
        text = ';'.join(css)
        if text:
            text += ';'
        return text

    def apply_template(self, view, css, css_type, template_vars=None):
        """Apply template to CSS."""

        self.view = view

        if css_type not in (POPUP, PHANTOM, SHEET):
            return ''

        self.css_type = css_type
        self.variables = self.get_variables()

        var = copy.copy(self.variables)
        if template_vars and isinstance(template_vars, (dict, OrderedDict)):
            self.plugin_vars = copy.deepcopy(template_vars)
        else:
            self.plugin_vars = {}

        var.update(
            {
                'is_phantom': self.css_type == PHANTOM,
                'is_popup': self.css_type == POPUP,
                'is_sheet': self.css_type == SHEET
            }
        )

        return self.env.from_string(css).render(var=var, plugin=self.plugin_vars)


def get_pygments(style):
    """
    Get Pygments style.

    Sublime CSS support is limited.  It cannot handle well
    things like: `.class1 .class2`,  but it can handle things like:
    `.class1.class2`.  So we will not use things like `.highlight` in front.

    We will first find {...} which has no syntax class.  This will contain
    our background and possibly foreground.  If for whatever reason we
    have no background or foreground, we will use `#000000` or `#ffffff`
    respectively.
    """

    try:
        # Lets see if we can find the Pygments theme
        text = HtmlFormatter(style=style).get_style_defs('.dummy')
        text = re_missing_semi_colon.sub('; }', text)
    except Exception:
        return ''

    bg = None
    fg = None

    # Find {...} which has no syntax classes
    m = re_base_colors.search(text)
    if m:
        # Find background
        m1 = re_bgcolor.search(m.group(1))
        if m1:
            # Use `background-color` as it works better
            # with Sublime CSS
            bg = m1.group(1).replace('background', 'background-color')
        # Find foreground
        m1 = re_color.search(m.group(1))
        if m1:
            fg = m1.group(1)
    # Use defaults if None found
    if bg is None:
        bg = 'background-color: #ffffff'
    if fg is None:
        fg = 'color: #000000'

    # Reassemble replacing .highlight {...} with `.codehilite`, `.inlinehilite` {...}
    # All other classes will be left bare with only their syntax class.
    code_blocks = CODE_BLOCKS
    if m:
        css = clean_css(
            (
                text[:m.start(0)] +
                (code_blocks.format(bg, fg)) +
                text[m.end(0):] +
                '\n'
            )
        )
    else:
        css = clean_css(
            (
                (code_blocks.format(bg, fg)) + '\n' + text + '\n'
            )
        )

    return re_pygments_selectors.sub(r'.mdpopups .highlight \1', css)
