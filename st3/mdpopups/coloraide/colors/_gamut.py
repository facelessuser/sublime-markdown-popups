"""Gamut handling."""
from .. import util
from . _range import Angle


class GamutBound(tuple):
    """Bounded gamut value."""


class GamutUnbound(tuple):
    """Unbounded gamut value."""


def lch_chroma(base, color):
    """
    Gamut mapping via chroma LCH.

    Algorithm comes from https://colorjs.io/docs/gamut-mapping.html.

    The idea is to hold hue and lightness constant and decrease lightness until
    color comes under gamut.

    We'll use a binary search and at after each stage, we will clip the color
    and compare the distance of the two colors (clipped and current color via binary search).
    If the distance is less than two, we can return the clipped color.

    ---
    Original Authors: Lea Verou, Chris Lilley
    License: MIT (As noted in https://github.com/LeaVerou/color.js/blob/master/package.json)
    """

    # Compare clipped against original to
    # judge how far we are off with the worst case fitting
    space = color.space()
    clipped = color.clone()
    clipped.fit(space=space, method="clip", in_place=True)
    base_error = base.delta(clipped, method="2000")

    if base_error > 2.3:
        threshold = .001
        # Compare mapped against desired space
        mapcolor = color.convert("lch")
        error = base_error
        low = 0.0
        high = mapcolor.chroma

        # Adjust chroma (using binary search).
        # This helps preserve the color more (in most cases).
        # After each adjustment, see if clipping gets us close enough.
        while (high - low) > threshold and error < base_error:
            clipped = mapcolor.clone()
            clipped.fit(space, method="clip", in_place=True)
            delta = mapcolor.delta(clipped, method="2000")
            error = color.delta(mapcolor, method="2000")
            if delta - 2 < threshold:
                low = mapcolor.chroma
            else:
                if abs(delta - 2) < threshold:
                    break
                high = mapcolor.chroma
            mapcolor.chroma = (high + low) / 2
        # Trim off noise allowed by our tolerance
        color.update(mapcolor)
        color.fit(space, method="clip", in_place=True)
    else:
        # We are close enough that we should just clip.
        color.update(clipped)
    return color.coords()


def clip(base, color):
    """Gamut clipping."""

    channels = color.coords()
    gamut = color._range
    fit = []

    for i, value in enumerate(channels):
        a, b = gamut[i]
        is_bound = isinstance(gamut[i], GamutBound)

        # Wrap the angle. Not technically out of gamut, but we will clean it up.
        if isinstance(a, Angle) and isinstance(b, Angle):
            fit.append(value if 0.0 <= value <= 360.0 else value % 360.0)
            continue

        # These parameters are unbounded
        if not is_bound:
            a = None
            b = None

        # Fit value in bounds.
        fit.append(util.clamp(value, a, b))
    return fit


class Gamut:
    """Gamut handling."""

    def fit_coords(self, space=None, *, method=None):
        """Get coordinates within this space or fit to another space."""

        if method is None:
            method = self.get_default("fit")

        space = (self.space() if space is None else space).lower()
        method = self.space() if method is None else method
        if not self.in_gamut(space=space):
            clone = self.clone()
            clone.fit(method=method, in_place=True)
            return clone.coords()
        return self.coords()

    def fit(self, space=None, *, method=None, in_place=False):
        """Fit the gamut using the provided method."""

        if method is None:
            method = self.get_default("fit")

        this = self if in_place else self.clone()

        # Select appropriate mapping algorithm
        if method == "clip":
            func = clip
        elif method == "lch-chroma":
            func = lch_chroma
        else:
            # Unknown fit method
            raise ValueError("'{}' gamut mapping is not currently supported".format(method))

        # Convert to desired space
        if space is not None:
            c = self.convert(space)
        else:
            c = self.clone()

        # If we are perfectly in gamut, don't waste time fitting
        if c.in_gamut(tolerance=0.0):
            this.update(c)
            return this

        # Apply mapping/clipping/etc.
        fit = func(self.clone(), c)
        for i in range(len(fit)):
            c._coords[i] = fit[i]

        # Adjust "this" color
        this.update(c)
        return this

    def in_gamut(self, space=None, *, tolerance=util.DEF_FIT_TOLERANCE):
        """Check if current color is in gamut."""

        # Check gamut in the provided space
        if space is not None:
            c = self.convert(space)
            return c.in_gamut()

        # Verify the values are in bound
        channels = self.coords()
        for i, value in enumerate(channels):
            a, b = self._range[i]
            is_bound = isinstance(self._range[i], GamutBound)

            # Angles will wrap, so no sense checking them
            if isinstance(a, Angle) and isinstance(b, Angle):
                continue

            # These parameters are unbounded
            if not is_bound:
                a = None
                b = None

            # Check if bounded values are in bounds
            if (a is not None and value < (a - tolerance)) or (b is not None and value > (b + tolerance)):
                return False

        return True
