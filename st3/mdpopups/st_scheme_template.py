"""
Sublime Text Scheme template.

Converts scheme to css provides templating for
additonal so that they can access the colors.

Licensed under MIT
Copyright (c) 2015 - 2016 Isaac Muse <isaacmuse@gmail.com>

----------------------

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions
"""
import sublime
import re
from .rgba import RGBA
from .st_color_scheme_matcher import ColorSchemeMatcher
import jinja2
from pygments.formatters import HtmlFormatter
from collections import OrderedDict
from .st_clean_css import clean_css
import copy
import decimal

INVALID = -1
POPUP = 0
PHANTOM = 1
LUM_MIDPOINT = 127

re_float_trim = re.compile(r'^(?P<keep>\d+)(?P<trash>\.0+|(?P<keep2>\.\d*[1-9])0+)$')
re_valid_custom_scopes = re.compile(r'[a-zA-Z\d]+[a-zA-Z\d._\-]*')

textmate_scopes = [
    'comment',
    'comment.line',
    'comment.line.double-slash',
    'comment.line.double-dash',
    'comment.line.number-sign',
    'comment.line.percentage',
    'comment.line.character',
    'comment.block',
    'comment.block.documentation',
    'constant',
    'constant.numeric',
    'constant.character',
    'constant.language',
    'constant.other',
    'entity',
    'entity.name',
    'entity.name.function',
    'entity.name.type',
    'entity.name.tag',
    'entity.name.section',
    'entity.other',
    'entity.other.inherited-class',
    'entity.other.attribute-name',
    'invalid',
    'invalid.illegal',
    'invalid.deprecated',
    'keyword',
    'keyword.control',
    'keyword.operator',
    'keyword.other',
    'markup',
    'markup.underline',
    'markup.underline.link',
    'markup.bold',
    'markup.heading',
    'markup.italic',
    'markup.list',
    'markup.list.numbered',
    'markup.list.unnumbered',
    'markup.quote',
    'markup.raw',
    'markup.other',
    'meta',
    'storage',
    'storage.type',
    'storage.modifier',
    'string',
    'string.quoted',
    'string.quoted.single',
    'string.quoted.double',
    'string.quoted.triple',
    'string.quoted.other',
    'string.unquoted',
    'string.interpolated',
    'string.regexp',
    'string.other',
    'support',
    'support.function',
    'support.class',
    'support.type',
    'support.constant',
    'support.variable',
    'support.other',
    'variable.parameter',
    'variable.language',
    'variable.other'
]

re_base_colors = re.compile(r'^\s*\.dummy\s*\{([^}]+)\}', re.MULTILINE)
re_color = re.compile(r'(?<!-)(color\s*:\s*#[A-Fa-z\d]{6})')
re_bgcolor = re.compile(r'(?<!-)(background(?:-color)?\s*:\s*#[A-Fa-z\d]{6})')
CODE_BLOCKS = '.highlight, .inline-highlight { %s; %s; }'


def fmt_float(f, p=0):
    """Set float precision and trim precision zeros."""

    string = str(
        decimal.Decimal(f).quantize(decimal.Decimal('0.' + ('0' * p) if p > 0 else '0'), decimal.ROUND_HALF_UP)
    )

    m = re_float_trim.match(string)
    if m:
        string = m.group('keep')
        if m.group('keep2'):
            string += m.group('keep2')
    return string


class Scheme2CSS(object):
    """Determine color scheme colors and style for text in a Sublime view buffer."""

    def __init__(self, scheme_file):
        """Initialize."""

        self.csm = ColorSchemeMatcher(scheme_file)
        self.text = ''
        self.colors = OrderedDict()
        self.scheme_file = scheme_file
        self.css_type = INVALID
        self.gen_css()

    def guess_style(self, scope, selected=False, explicit_background=False):
        """Guess color."""

        return self.csm.guess_color(scope, selected, explicit_background)

    def parse_global(self):
        """Parse global settings."""

        color_settings = {}
        for item in self.csm.plist_file["settings"]:
            if item.get('scope', None) is None and item.get('name', None) is None:
                color_settings = item["settings"]
                break

        # Get general theme colors from color scheme file
        self.bground = self.strip_color(color_settings.get("background", '#FFFFFF'), simple_strip=True)
        rgba = RGBA(self.bground)
        self.lums = rgba.get_luminance()
        is_dark = self.lums <= LUM_MIDPOINT
        self.variables = {
            "is_dark": is_dark,
            "is_light": not is_dark,
            "color_scheme": self.scheme_file,
            "use_pygments": not sublime.load_settings("Preferences.sublime-settings").get(
                'mdpopups.use_sublime_highlighter', False
            )
        }
        self.html_border = rgba.get_rgb()
        self.fground = self.strip_color(color_settings.get("foreground", '#000000'))

        # Intialize colors with the global foreground, background, and fake html_border
        self.colors = OrderedDict()
        self.colors['.foreground'] = OrderedDict([('color', 'color: %s; ' % self.fground)])
        self.colors['.background'] = OrderedDict([('background-color', 'background-color: %s; ' % self.bground)])

    def parse_settings(self):
        """Parse the color scheme."""

        for tscope in textmate_scopes:
            scope = self.guess_style(tscope, explicit_background=True)
            key_scope = '.' + tscope
            color = scope.fg_simulated
            bgcolor = scope.bg_simulated
            if color or bgcolor:
                self.colors[key_scope] = OrderedDict()
                if color:
                    self.colors[key_scope]['color'] = 'color: %s; ' % color
                if bgcolor:
                    self.colors[key_scope]['background-color'] = 'background-color: %s; ' % bgcolor

                for s in scope.style.split(' '):
                    if "bold" in s:
                        self.colors[key_scope]['font-weight'] = 'font-weight: %s; ' % 'bold'
                    if "italic" in s:
                        self.colors[key_scope]['font-style'] = 'font-style: %s; ' % 'italic'
                    if "underline" in s and False:  # disabled
                        self.colors[key_scope]['text-decoration'] = 'text-decoration: %s; ' % 'underline'

    def strip_color(self, color, simple_strip=False):
        """
        Strip transparency from the color value.

        Transparency can be stripped in one of two ways:
            - Simply mask off the alpha channel.
            - Apply the alpha channel to the color essential getting the color seen by the eye.
        """

        if color is None or color.strip() == "":
            return None

        rgba = RGBA(color.replace(" ", ""))
        if not simple_strip:
            rgba.apply_alpha(self.bground if self.bground != "" else "#FFFFFF")

        return rgba.get_rgb()

    def gen_css(self):
        """Generate the CSS and the associated template environment."""

        self.colors = OrderedDict()
        self.parse_global()
        self.parse_settings()

        # Assemble the CSS text
        text = []
        for k, v in self.colors.items():
            text.append('%s { %s}' % (k, ''.join(v.values())))
        self.text = '\n'.join(text)

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
        self.env.filters['grayscale'] = self.grayscale
        self.env.filters['sepia'] = self.sepia
        self.env.filters['fade'] = self.fade
        self.env.filters['getcss'] = self.read_css
        self.env.filters['relativesize'] = self.relativesize

    def read_css(self, css):
        """Read the CSS file."""

        try:
            var = copy.copy(self.variables)
            var.update(
                {
                    'is_phantom': self.css_type == PHANTOM,
                    'is_popup': self.css_type == POPUP
                }
            )

            return self.env.from_string(clean_css(sublime.load_resource(css))).render(var=var, colors=self.colors)
        except Exception:
            return ''

    def relativesize(self, css, *args):
        """Create a relative font from the current font."""

        # Handle things the new way '+1.25em'
        try:
            if css.endswith(('em', 'px', 'pt')):
                offset = css[:-2]
                unit = css[-2:]
                integer = bool(len(args) and args[0])
            else:
                offset = css
                unit = args[0]
                integer = False
                assert isinstance(unit, str) and unit in ('em', 'px', 'pt'), 'Bad Arguments!'
        except Exception:
            return css

        if unit == 'em':
            size = self.font_size / 16.0
        elif unit == 'px':
            size = self.font_size
        elif unit == 'pt':
            size = (self.font_size / 16.0) * 12.0

        precision = 0 if integer else 3

        op = offset[0]
        if op in ('+', '-', '*'):
            value = size * float(offset[1:]) if op == '*' else size + float(offset)
        else:
            value = 0.0

        if value < 0.0:
            value = 0.0

        return '%s%s' % (fmt_float(value, precision), unit)

    def fade(self, css, factor):
        """
        Apply a fake transparency to color.

        Fake transparency is preformed on top of the background color.
        """
        try:
            parts = [c.strip('; ') for c in css.split(':')]
            if len(parts) == 2 and parts[0] in ('background-color', 'color'):
                bgcolor = self.colors.get('.background').get('background-color')
                bgparts = [c.strip('; ') for c in bgcolor.split(':')]
                rgba = RGBA(parts[1] + "%02f" % int(255.0 * max(min(float(factor), 1.0), 0.0)))
                rgba.apply_alpha(bgparts[1])
                return '%s: %s; ' % (parts[0], rgba.get_rgb())
        except Exception:
            pass
        return css

    def colorize(self, css, degree):
        """Colorize to the given hue."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.colorize(degree)
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def hue(self, css, degree):
        """Shift hue."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.hue(degree)
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def invert(self, css):
        """Invert color."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.invert()
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def saturation(self, css, factor):
        """Apply saturation filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.saturation(factor)
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def grayscale(self, css):
        """Apply grayscale filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.grayscale()
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def sepia(self, css):
        """Apply sepia filter."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.sepia()
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def brightness(self, css, factor):
        """Adjust brightness."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] in ('background-color', 'color'):
            rgba = RGBA(parts[1])
            rgba.brightness(factor)
            parts[1] = "%s; " % rgba.get_rgb()
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def to_fg(self, css):
        """Rename a CSS key value pair."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] == 'background-color':
            parts[0] = 'color'
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def to_bg(self, css):
        """Rename a CSS key value pair."""

        parts = [c.strip('; ') for c in css.split(':')]
        if len(parts) == 2 and parts[0] == 'color':
            parts[0] = 'background-color'
            return '%s: %s ' % (parts[0], parts[1])
        return css

    def pygments(self, style):
        """Get pygments style."""

        return get_pygments(style)

    def retrieve_selector(self, selector, key=None):
        """Get the CSS key, value pairs for a rule."""

        wanted = [s.strip() for s in selector.split(',')]
        sel = {}
        for w in wanted:
            if w in self.colors:
                sel = self.colors[w]
                break
        return ''.join(sel.values()) if key is None else sel.get(key, '')

    def get_font_scale(self):
        """Get font scale."""

        scale = 1.0
        try:
            pref_scale = float(sublime.load_settings('Preferences.sublime-settings').get('mdpopups.font_scale', 0.0))
        except Exception:
            pref_scale = 0.0

        if sublime.platform() == 'windows' and pref_scale <= 0.0:
            try:
                import ctypes

                logpixelsy = 90
                dc = ctypes.windll.user32.GetDC(0)
                height = ctypes.windll.gdi32.GetDeviceCaps(dc, logpixelsy)
                scale = float(height) / 96.0
                ctypes.windll.user32.ReleaseDC(0, dc)
            except Exception:
                pass
        elif pref_scale > 0.0:
            scale = pref_scale

        return scale

    def apply_template(self, css, css_type, font_size):
        """Apply template to css."""

        if css_type not in (POPUP, PHANTOM):
            return ''

        self.font_size = float(font_size) * self.get_font_scale()
        self.css_type = css_type

        var = copy.copy(self.variables)
        var.update(
            {
                'is_phantom': self.css_type == PHANTOM,
                'is_popup': self.css_type == POPUP
            }
        )

        return self.env.from_string(css).render(var=var, colors=self.colors)

    def get_css(self):
        """Get css."""

        return self.text


def get_pygments(style):
    """
    Get pygments style.

    Subllime CSS support is limited.  It cannot handle well
    things like: `.class1 .class2`,  but it can handle things like:
    `.class1.class2`.  So we will not use things like `.highlight` in front.

    We will first find {...} which has no syntax class.  This will contain
    our background and possibly foreground.  If for whatever reason we
    have no background or foreground, we will use `#000000` or `#ffffff`
    respectively.
    """

    try:
        # Lets see if we can find the pygments theme
        text = HtmlFormatter(style=style).get_style_defs('.dummy')
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

    # Reassemble replacing .highlight {...} with .codehilite, .inlinehilite {...}
    # All other classes will be left bare with only their syntax class.
    if m:
        css = clean_css(
            (
                text[:m.start(0)] +
                (CODE_BLOCKS % (bg, fg)) +
                text[m.end(0):] +
                '\n'
            ).replace('.dummy ', '')
        )
    else:
        css = clean_css(
            (
                (CODE_BLOCKS % (bg, fg)) + '\n' + text + '\n'
            )
        ).replace('.dummy ', '')
    return css
