"""
SublimeHighlight.

Licensed under MIT.

Copyright (C) 2012  Andrew Gibson <agibsonsw@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---------------------

Original code has been heavily modifed by Isaac Muse <isaacmuse@gmail.com> for the ExportHtml project.
"""
import sublime
import re
from .st_color_scheme_matcher import ColorSchemeMatcher
from .st_mapping import lang_map

INLINE_BODY_START = '<code class="inline-highlight">'
BODY_START = '<div class="highlight"><pre>'
LINE = '%(code)s<br>'
CODE = '<span %(class)sstyle="color: %(color)s;">%(content)s</span>'
CODEBG = '<span %(class)sstyle="background-color: %(highlight)s; color: %(color)s;">%(content)s</span>'
BODY_END = '</pre></div>\n'
INLINE_BODY_END = '</code>'

USE_ST_SYNTAX = int(sublime.version()) >= 3084
ST_LANGUAGES = ('.sublime-syntax', '.tmLanguage') if USE_ST_SYNTAX else ('.tmLanguage',)


class SublimeHighlight(object):
    """SublimeHighlight."""

    def __init__(self, scheme):
        """Initialization."""

        self.view = None
        self.csm = ColorSchemeMatcher(scheme)

        (
            self.bground, self.fground, self.sbground, self.sfground
        ) = self.csm.get_general_colors(simulate_transparency=True)

    def setup(self, **kwargs):
        """Get get general document preferences from sublime preferences."""

        settings = sublime.load_settings('Preferences.sublime-settings')
        self.tab_size = settings.get('tab_size', 4)
        # self.char_limit = 4
        self.bground = ''
        self.fground = ''
        self.sbground = ''
        self.sfground = ''
        self.sels = []
        # self.multi_select = False
        self.highlight_selections = False
        self.hl_continue = None
        self.curr_hl = None
        self.size = self.view.size()
        self.pt = 0
        self.end = 0
        self.curr_row = 0
        self.tables = 0
        self.matched = {}
        self.ebground = self.bground

        self.highlights = []
        if self.highlight_selections:
            for sel in self.view.sel():
                if not sel.empty():
                    self.highlights.append(sel)

    def setup_print_block(self, curr_sel, multi=False):
        """Determine start and end points and whether to parse whole file or selection."""

        self.size = self.view.size()
        self.pt = 0
        self.end = 1
        self.curr_row = 1
        self.start_line = self.curr_row

    def print_line(self, line, num):
        """Print the line."""

        html_line = LINE % {
            "code": line,
        }

        return html_line

    def convert_view_to_html(self):
        """Begin conversion of the view to HTML."""

        for line in self.view.split_by_newlines(sublime.Region(self.pt, self.size)):
            self.size = line.end()
            empty = not bool(line.size())
            line = self.convert_line_to_html(empty)
            self.html.append(self.print_line(line, self.curr_row))
            self.curr_row += 1

    def html_encode(self, text):
        """Format text to HTML."""
        encode_table = {
            '&': '&amp;',
            '>': '&gt;',
            '<': '&lt;',
            '\t': ' ' * self.tab_size,
            '\n': ''
        }

        return re.sub(
            r'(?!\s($|\S))\s',
            '&nbsp;',
            ''.join(
                encode_table.get(c, c) for c in text
            )
        )

    def format_text(self, line, text, color, bgcolor, style, empty, annotate=False):
        """Format the text."""

        if empty:
            text = '&nbsp;'

        if self.inline:
            style += " inline-highlight"

        if bgcolor is None:
            code = CODE % {
                "color": color, "content": text,
                "class": "class=\"%s\" " % style if style else ''
            }
        else:
            code = CODEBG % {
                "highlight": bgcolor, "color": color, "content": text,
                "class": "class=\"%s\" " % style if style else ''
            }

        line.append(code)

    def convert_line_to_html(self, empty):
        """Convert the line to its HTML representation."""

        line = []
        hl_done = False

        # Continue highlight form last line
        if self.hl_continue is not None:
            self.curr_hl = self.hl_continue
            self.hl_continue = None

        while self.end <= self.size:
            # Get next highlight region
            if self.highlight_selections and self.curr_hl is None and len(self.highlights) > 0:
                self.curr_hl = self.highlights.pop(0)

            # See if we are starting a highlight region
            if self.curr_hl is not None and self.pt == self.curr_hl.begin():
                # Get text of like scope up to a highlight
                scope_name = self.view.scope_name(self.pt)
                while self.view.scope_name(self.end) == scope_name and self.end < self.size:
                    # Kick out if we hit a highlight region
                    if self.end == self.curr_hl.end():
                        break
                    self.end += 1
                if self.end < self.curr_hl.end():
                    if self.end >= self.size:
                        self.hl_continue = sublime.Region(self.end, self.curr_hl.end())
                    else:
                        self.curr_hl = sublime.Region(self.end, self.curr_hl.end())
                else:
                    hl_done = True
                if hl_done and empty:
                    color_match = self.csm.guess_color(self.view, self.pt, scope_name)
                    color = color_match.fg_simulated
                    style = color_match.style
                    bgcolor = color_match.bg_simulated
                elif self.sfground is None:
                    color_match = self.csm.guess_color(self.view, self.pt, scope_name)
                    color = color_match.fg_simulated
                    style = color_match.style
                    bgcolor = self.sbground
                else:
                    color, style = self.sfground, ""
                    bgcolor = self.sbground
            else:
                # Get text of like scope up to a highlight
                scope_name = self.view.scope_name(self.pt)
                while self.view.scope_name(self.end) == scope_name and self.end < self.size:
                    # Kick out if we hit a highlight region
                    if self.curr_hl is not None and self.end == self.curr_hl.begin():
                        break
                    self.end += 1
                color_match = self.csm.guess_color(self.view, self.pt, scope_name)
                color = color_match.fg_simulated
                style = color_match.style
                bgcolor = color_match.bg_simulated

            region = sublime.Region(self.pt, self.end)
            # Normal text formatting
            tidied_text = self.html_encode(self.view.substr(region))
            self.format_text(line, tidied_text, color, bgcolor, style, empty)

            if hl_done:
                # Clear highlight flags and variables
                hl_done = False
                self.curr_hl = None

            # Continue walking through line
            self.pt = self.end
            self.end = self.pt + 1

        # Get the color for the space at the end of a line
        if self.end < self.view.size():
            end_key = self.view.scope_name(self.pt)
            color_match = self.csm.guess_color(self.view, self.pt, end_key)
            self.ebground = color_match.bg_simulated

        # Join line segments
        return ''.join(line)

    def write_body(self):
        """Write the body of the HTML."""

        processed_rows = ""
        self.html.append(INLINE_BODY_START if self.inline else BODY_START)

        # Convert view to HTML
        self.setup_print_block(self.view.sel()[0])
        processed_rows += "[" + str(self.curr_row) + ","
        self.convert_view_to_html()
        processed_rows += str(self.curr_row) + "],"
        self.tables += 1

        # Write empty line to allow copying of last line and line number without issue
        self.html.append(INLINE_BODY_END if self.inline else BODY_END)

    def set_view(self, src, lang):
        """Setup view for conversion."""

        # Get the output panel
        self.view = sublime.active_window().get_output_panel('mdpopups')
        # Let all plugins no to leave this view alone
        self.view.settings().set('is_widget', True)
        # Don't translate anything.
        self.view.settings().set("translate_tabs_to_spaces", False)
        # Don't mess with my indenting Sublime!
        self.view.settings().set("auto_indent", False)
        # Insert into the view
        self.view.run_command('insert', {'characters': src})
        # Setup the proper syntax
        lang = lang.lower()
        user_map = sublime.load_settings('Preferences.sublime-settings').get('mdpopups_sublime_user_lang_map', {})
        loaded = False
        for k, v in lang_map.items():
            user_v = user_map.get(k, (tuple(), tuple()))
            if lang in (user_v[0] + v[0]):
                for l in (user_v[1] + v[1]):
                    for ext in ST_LANGUAGES:
                        sytnax_file = 'Packages/%s%s' % (l, ext)
                        try:
                            sublime.load_binary_resource(sytnax_file)
                        except Exception:
                            continue
                        self.view.set_syntax_file(sytnax_file)
                        loaded = True
                        break
            if loaded:
                break

    def syntax_highlight(self, src, lang, inline=False):
        """Syntax Highlight."""

        self.set_view(src, lang)
        self.inline = inline
        self.setup()
        self.html = []
        self.write_body()
        return ''.join(self.html)
