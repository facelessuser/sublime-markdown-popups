"""LCH class."""
from ._space import Space, RE_DEFAULT_MATCH
from ._cylindrical import Cylindrical
from ._gamut import GamutUnbound
from . _range import Angle, Percent
from . import _convert as convert
from . import _parse as parse
from .. import util
import re


class LCH(Cylindrical, Space):
    """LCH class."""

    SPACE = "lch"
    DEF_BG = "color(lch 0 0 0 / 1)"
    CHANNEL_NAMES = frozenset(["lightness", "chroma", "hue", "alpha"])
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space=SPACE))

    _range = (
        # I think chroma, specifically should be clamped.
        # Some libraries don't to prevent rounding issues. We should only get
        # negative chroma via direct user input, but when translating to
        # Lab, this will be corrected.
        GamutUnbound([Percent(0.0), Percent(100.0)]),
        GamutUnbound([0.0, 100.0]),
        GamutUnbound([Angle(0.0), Angle(360.0)]),
    )

    def __init__(self, color=DEF_BG):
        """Initialize."""

        super().__init__(color)

        if isinstance(color, Space):
            self.lightness, self.chroma, self.hue = convert.convert(color.coords(), color.space(), self.space())
            self.alpha = color.alpha
        elif isinstance(color, str):
            values = self.match(color)[0]
            if values is None:
                raise ValueError("'{}' does not appear to be a valid color".format(color))
            self.lightness, self.chroma, self.hue, self.alpha = values
        elif isinstance(color, (list, tuple)):
            if not (3 <= len(color) <= 4):
                raise ValueError("A list of channel values should be of length 3 or 4.")
            self.lightness = color[0]
            self.chroma = color[1]
            self.hue = color[2]
            self.alpha = 1.0 if len(color) == 3 else color[3]
        else:
            raise TypeError("Unexpected type '{}' received".format(type(color)))

    def is_hue_null(self):
        """Test if hue is null."""

        l, c, h = self.coords()
        return c < util.ACHROMATIC_THRESHOLD

    def hue_index(self):
        """Get hue index."""

        return 2

    @property
    def lightness(self):
        """Lightness."""

        return self._coords[0]

    @lightness.setter
    def lightness(self, value):
        """Get true luminance."""

        self._coords[0] = self._handle_input(value)

    @property
    def chroma(self):
        """Chroma."""

        return self._coords[1]

    @chroma.setter
    def chroma(self, value):
        """chroma."""

        self._coords[1] = self._handle_input(value)

    @property
    def hue(self):
        """Hue."""

        return self._coords[2]

    @hue.setter
    def hue(self, value):
        """Shift the hue."""

        self._coords[2] = self._handle_input(value)

    @classmethod
    def translate_channel(cls, channel, value):
        """Translate channel string."""

        if channel in (0, 1):
            return parse.norm_float(value)
        elif channel == 2:
            return parse.norm_deg_channel(value)
        elif channel == -1:
            return parse.norm_alpha_channel(value)
        else:
            raise ValueError("Unexpected channel index of '{}'".format(channel))

    def to_string(self, *, alpha=None, precision=util.DEF_PREC, fit=True, **kwargs):
        """To string."""

        return super().to_string(alpha=alpha, precision=precision, fit=fit)
