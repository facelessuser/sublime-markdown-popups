"""
Github flavored markdown
~~~~~~~~~~~~~~~~~~~~~~~~

https://github.github.com/gfm

Unlike other extensions, GFM provides a self-contained subclass of ``Markdown``
with parser and renderer already set.
User may also use the parser and renderer as bases for further extension.

Example usage::

    from marko.ext.gfm import gfm
    print(gfm(text))

"""

from ..marko import Markdown
from ..marko.helpers import MarkoExtension, render_dispatch
from ..marko.html_renderer import HTMLRenderer
from ..marko.ext.gfm import elements, renderer


class GFMRendererMixin(renderer.GFMRendererMixin):
    """GFM renderer with changes needed for Sublime."""

    @render_dispatch(HTMLRenderer)
    def render_alert(self, element):
        """Render alert with explicit title class."""

        header = self.escape_html(element.alert_type)
        children = self.render_children(element)
        return (
            f'<blockquote class="alert alert-{element.alert_type.lower()}">\n'
            f'<p class="alert-title">{header.title()}</p>\n{children}</blockquote>\n'
        )


GFM = MarkoExtension(
    elements=[
        elements.Paragraph,
        elements.Strikethrough,
        elements.Url,
        # elements.Table,
        # elements.TableRow,
        # elements.TableCell,
        elements.Alert,
    ],
    renderer_mixins=[GFMRendererMixin],
)


gfm = Markdown(extensions=[GFM])


def make_extension():
    return GFM
