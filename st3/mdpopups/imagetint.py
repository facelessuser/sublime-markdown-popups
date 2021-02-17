"""
Image tinting.

Licensed under MIT
Copyright (c) 2015 - 2020 Isaac Muse <isaacmuse@gmail.com>
"""
from .png import Reader, Writer
from .coloraide import Color, util
import base64
import io


def tint_raw(byte_string, color, opacity=255):
    """Tint the image and return a byte string."""

    # Read the byte string as a RGBA image.
    width, height, pixels, meta = Reader(bytes=byte_string).asRGBA()

    # Clamp opacity
    if opacity < 0:
        opacity = 0
    elif opacity > 255:
        opacity = 255

    # Tint
    p = []
    y = 0
    for row in pixels:
        p.append([])
        columns = int(len(row) / 4)
        start = 0
        for x in range(columns):
            rgba = Color(color)
            rgba.alpha = opacity / 255.0
            rgba.overlay(background='#{:02X}{:02X}{:02X}FF'.format(*row[start:start + 3]))
            rgba.fit(in_place=True)
            p[y] += [
                int(util.round_half_up(rgba.red * 255)),
                int(util.round_half_up(rgba.green * 255)),
                int(util.round_half_up(rgba.blue * 255)),
                row[start + 3]
            ]
            start += 4
        y += 1

    # Create bytes buffer for PNG
    with io.BytesIO() as f:

        # Write out PNG
        img = Writer(width, height, alpha=True)
        img.write(f, p)

        # Read out PNG bytes and base64 encode
        f.seek(0)

        return f.read()


def tint(byte_string, color, opacity=255, height=None, width=None):
    """Base64 encode the tint."""

    style = ''
    if width:
        style = 'style="width: {:d}px;"'.format(width)
    if height is not None and style is None:
        style = 'style="height: {:d}px;"'.format(width)
    elif height is not None:
        style = style[:-1] + (' height: {:d}px;" '.format(height))

    return '<img {}src="data:image/png;base64,{}">'.format(
        style,
        base64.b64encode(tint_raw(byte_string, color, opacity)).decode('ascii')
    )
