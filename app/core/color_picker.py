#!/home/vueko/Projetos/py_rgb/.venv/bin/python3
from enum import Enum

from colour import Color
from openrgb.utils import RGBColor


class Colors(Enum):
    red = "#FF0000"
    blue = "#0000FF"
    green = "#00FF00"
    purple = "#8800FF"
    yellow = "#FFFF00"
    cian = "#41FFFF"
    orange = "#FF3000"
    white = "#FFFFFF"

    @classmethod
    def gradient(cls, _from: str, to: str, steps: int) -> list[Color]:
        origin = Color(_from)
        destination = Color(to)

        return list(origin.range_to(destination, steps=steps))  # type: ignore

    @classmethod
    def gradient_rgb_color(cls, _from: str, to: str, steps: int) -> list[RGBColor]:
        Colors.gradient(_from, to, steps)
        return [
            RGBColor.fromHEX(color.get_hex_l())
            for color in Colors.gradient(_from, to, steps)
        ]  # type: ignore
