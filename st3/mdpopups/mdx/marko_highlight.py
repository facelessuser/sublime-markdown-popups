r"""
Code highlight extension.

Enable code highlight using `pygments`. This requires to install `codehilite` extras::

    ```
    pip install marko[codehilite]
    ```

Arguments:
    All arguments are passed to `pygments.formatters.html.HtmlFormatter`.

Usage::

    ````
    from marko import Markdown

    markdown = Markdown(extensions=['codehilite'])
    markdown.convert('```python filename="my_script.py"\nprint('hello world')\n```')
    ````
"""
import re
from ..marko import HTMLRenderer
from ..marko.helpers import MarkoExtension, render_dispatch
from ..st_pygments_highlight import syntax_hl

HL_SETTING = 'mdpopups.use_sublime_highlighter'
multi_space = re.compile(r'(?<= ) {2,}')


class CodeHiliteRendererMixin:
    """Code highlighting extension."""

    options = {}  # type: dict
    st_hl = None
    st_wrap = False
    st_lang_map = {}

    @render_dispatch(HTMLRenderer)
    def render_fenced_code(self, element):
        """Render the fenced code."""

        code = element.children[0].children
        if self.st_hl is None:
            return syntax_hl(code, element.lang)
        return self.st_hl.syntax_highlight(code, element.lang, code_wrap=self.st_wrap, plugin_map=self.st_lang_map)


def make_extension(sublime_hl, sublime_wrap, sublime_lang_map, **options):
    """Return the extension."""

    class CodeMixin(CodeHiliteRendererMixin):
        """Modified extension."""

        st_hl = sublime_hl
        st_wrap = sublime_wrap
        st_lang_map = sublime_lang_map

    mixin_cls = type(
        "CodeHiliteRendererMixin", (CodeMixin,), {"options": options}
    )
    return MarkoExtension(renderer_mixins=[mixin_cls])
