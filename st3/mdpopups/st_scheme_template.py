"""
Sublime Text Scheme template.

Converts scheme to css provides templating for
additonal so that they can access the colors.

Licensed under MIT
Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

----------------------

TextMate theme to CSS.

https://manual.macromates.com/en/language_grammars#naming_conventions

Available scopes
================
foreground
background
comment
comment.line
comment.line.double-slash
comment.line.double-dash
comment.line.number-sign
comment.line.percentage
comment.line.character
comment.block
comment.block.documentation
constant
constant.numeric
constant.character
constant.language
constant.other
entity
entity.name
entity.other
invalid
invalid.illegal
invalid.deprecated
keyword
keyword.control
keyword.operator
keyword.other
markup
markup.underline
markup.underline.link
markup.bold
markup.heading
markup.italic
markup.list
markup.list.numbered
markup.list.unnumbered
markup.quote
markup.raw
markup.other
meta
storage
storage.type
storage.modifier
string
string.quoted
string.quoted.single
string.quoted.double
string.quoted.triple
string.quoted.other
string.unquoted
string.interpolated
string.regexp
string.other
support
support.function
support.class
support.type
support.constant
support.variable
support.other
variable.parameter
variable.language
variable.other
"""
import sublime
import re
from .rgba import RGBA
import os
import jinja2
from plistlib import readPlistFromBytes
from pygments.formatters import HtmlFormatter
from collections import OrderedDict
from .st_clean_css import clean_css

LUM_MIDPOINT = 127

re_textmate_scopes = re.compile(
    r'''(?x)^
    comment
      (?:\.(?:line(?:\.(?:double-slash|double-dash|number-sign|percentage|character))?|block(?:\.documentation)?))?|
    constant
      (?:\.(?:numeric|character|langauge|other))?|
    entity
      (?:\.(?:name|other))?|
    invalid
      (?:\.(?:illegal|deprecated))?|
    keyword
      (?:\.(?:control|operator|other))?|
    markup
      (?:\.(?:underline(?:\.link)?|link|bold|heading|italic|list(?:\.(?:numbered|unnumbered))?|quote|raw|other))?|
    meta|
    storage
      (?:\.(?:storage|type|modifier))?|
    string
      (?:\.(?:quoted(?:\.(?:single|double|triple|other))?|unquoted|interpolated|regexp|other))?|
    support
      (?:\.(?:function|class|type|constant|variable|other))?|
    variable
      (?:\.(?:parameter|language|other))?$
    '''
)

re_strip_xml_comments = re.compile(br"^[\r\n\s]*<!--[\s\S]*?-->[\s\r\n]*|<!--[\s\S]*?-->")
re_base_colors = re.compile(r'^\s*\.highlight\s*\{([^}]+)\}', re.MULTILINE)
re_color = re.compile(r'(?<!-)(color\s*:\s*#[A-Fa-z\d]{6})')
re_bgcolor = re.compile(r'(?<!-)(background(?:-color)?\s*:\s*#[A-Fa-z\d]{6})')
blocks = '.codehilite, .inlinehilite { %s; %s; }'


class Scheme2CSS(object):
    """Determine color scheme colors and style for text in a Sublime view buffer."""

    def __init__(self, scheme_file):
        """Initialize."""
        self.color_scheme = os.path.normpath(scheme_file)
        # self.scheme_file = os.path.basename(self.color_scheme)
        self.plist_file = readPlistFromBytes(
            re_strip_xml_comments.sub(
                b'',
                sublime.load_binary_resource(scheme_file)
            )
        )
        self.text = ''
        self.colors = OrderedDict()
        self.scheme_file = scheme_file
        self.gen_css()

    def parse_scheme(self):
        """Parse the color scheme."""

        color_settings = self.plist_file["settings"][0]["settings"]

        # Get general theme colors from color scheme file
        self.bground = self.strip_color(color_settings.get("background", '#FFFFFF'), simple_strip=True)
        rgba = RGBA(self.bground)
        self.lums = rgba.luminance()
        self.is_dark = self.lums <= LUM_MIDPOINT
        if self.is_dark:
            rgba.brightness(1.1)
        else:
            rgba.brightness(0.9)
        self.html_border = rgba.get_rgb()
        self.fground = self.strip_color(color_settings.get("foreground", '#000000'))

        # Create scope color mapping from color scheme file
        colors = OrderedDict()
        for item in self.plist_file["settings"]:
            name = item.get('name', None)
            scope = item.get('scope', None)
            color = None
            style = []
            if 'settings' in item:
                color = item['settings'].get('foreground', None)
                bgcolor = item['settings'].get('background', None)
                if 'fontStyle' in item['settings']:
                    for s in item['settings']['fontStyle'].split(' '):
                        if s == "bold" or s == "italic":  # or s == "underline":
                            style.append(s)

            if scope is not None and name is not None and (color is not None or bgcolor is not None):
                fg = self.strip_color(color)
                bg = self.strip_color(bgcolor)
                colors[scope] = {
                    "color": fg,
                    "bgcolor": bg,
                    "style": style
                }
        return colors

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
        """Get CSS."""

        colors = self.parse_scheme()
        self.colors = OrderedDict()
        self.colors['html'] = OrderedDict([('background-color', 'background-color: %s; ' % self.html_border)])
        self.colors['.foreground'] = OrderedDict([('color', 'color: %s; ' % self.fground)])
        self.colors['.background'] = OrderedDict([('background-color', 'background-color: %s; ' % self.bground)])

        for k, v in colors.items():
            for scope in [scope.strip() for scope in k.split(',')]:
                if ' ' in scope:
                    # Ignore complex scopes like:
                    #    "myscope.that.is way.to.complex" or "myscope.that.is -way.to.complex"
                    continue

                if re_textmate_scopes.match(scope):
                    key_scope = '.' + scope
                    self.colors[key_scope] = OrderedDict()
                    if v['color']:
                        self.colors[key_scope]['color'] = 'color: %s; ' % v['color']
                    if v['bgcolor']:
                        self.colors[key_scope]['background-color'] = 'background-color: %s; ' % v['bgcolor']
                    if 'italic' in v['style']:
                        self.colors[key_scope]['font-style'] = 'font-style: %s; ' % 'italic'
                    if 'bold' in v['style']:
                        self.colors[key_scope]['font-weight'] = 'font-weight: %s; ' % 'bold'

        text = []
        for k, v in self.colors.items():
            text.append('%s { %s}' % (k, ''.join(v.values())))
        self.text = '\n'.join(text)

        # Create Jinja template
        self.env = jinja2.Environment()
        self.env.filters['css'] = self.retrieve_selector
        self.env.filters['pygments'] = get_pygments

    def retrieve_selector(self, selector, key=None):
        """Get the CSS key, value pairs for a rule."""

        sel = self.colors.get(selector, {})
        return ''.join(sel.values()) if key is None else sel.get(key, '')

    def apply_template(self, css):
        """Apply template to css."""

        return self.env.from_string(css).render(css=self.colors)

    def get_css(self):
        """Get css."""

        return self.text


def get_pygments(style):
    """Get pygments style."""

    try:
        text = HtmlFormatter(style=style).get_style_defs('.highlight')
    except Exception:
        return ''

    bg = None
    fg = None

    # Find .highlight {} which has no syntax classes
    # This contains the background and possibly the foreground
    m = re_base_colors.search(text)
    if m:
        m1 = re_bgcolor.search(m.group(1))
        if m1:
            bg = m1.group(1).replace('background', 'background-color')
        m1 = re_color.search(m.group(1))
        if m1:
            fg = m1.group(1)
    if bg is None:
        bg = 'background-color: #ffffff'
    if fg is None:
        fg = 'color: #000000'

    # Reassemble replacing .highlight {} with .codehilite, .inlinehilite {}
    return clean_css(
        (
            text[:m.start(0)] +
            (blocks % (bg, fg)) +
            text[m.end(0):] +
            '\n'
        ).replace('.highlight ', '')
    )
