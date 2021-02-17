"""XYZ class."""
from ._space import Space, RE_DEFAULT_MATCH
from ._gamut import GamutUnbound
from . import _convert as convert
from . import _parse as parse
from .. import util
import re


class XYZ(Space):
    """XYZ class."""

    SPACE = "xyz"
    DEF_BG = "color(xyz 0 0 0 / 1)"
    CHANNEL_NAMES = frozenset(["x", "y", "z", "alpha"])
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space=SPACE))

    _range = (
        GamutUnbound([0.0, 1.0]),
        GamutUnbound([0.0, 1.0]),
        GamutUnbound([0.0, 1.0])
    )

    def __init__(self, color=DEF_BG):
        """Initialize."""

        super().__init__(color)

        if isinstance(color, Space):
            self.x, self.y, self.z = convert.convert(color.coords(), color.space(), self.space())
            self.alpha = color.alpha
        elif isinstance(color, str):
            values = self.match(color)[0]
            if values is None:
                raise ValueError("'{}' does not appear to be a valid color".format(color))
            self.x, self.y, self.z, self.alpha = values
        elif isinstance(color, (list, tuple)):
            if not (3 <= len(color) <= 4):
                raise ValueError("A list of channel values should be of length 3 or 4.")
            self.x = color[0]
            self.y = color[1]
            self.z = color[2]
            self.alpha = 1.0 if len(color) == 3 else color[3]
        else:
            raise TypeError("Unexpected type '{}' received".format(type(color)))

    @property
    def x(self):
        """X channel."""

        return self._coords[0]

    @x.setter
    def x(self, value):
        """Shift the X."""

        self._coords[0] = self._handle_input(value)

    @property
    def y(self):
        """Y channel."""

        return self._coords[1]

    @y.setter
    def y(self, value):
        """Set Y."""

        self._coords[1] = self._handle_input(value)

    @property
    def z(self):
        """Z channel."""

        return self._coords[2]

    @z.setter
    def z(self, value):
        """Set Z channel."""

        self._coords[2] = self._handle_input(value)

    @classmethod
    def translate_channel(cls, channel, value):
        """Translate channel string."""

        if channel in (0, 1, 2):
            return parse.norm_float(value)
        elif channel == -1:
            return parse.norm_alpha_channel(value)
        else:
            raise ValueError("Unexpected channel index of '{}'".format(channel))

    def to_string(self, *, options=None, alpha=None, precision=util.DEF_PREC, fit=True, **kwargs):
        """To string."""

        return super().to_string(alpha=alpha, precision=precision, fit=fit)
