#!/home/vueko/Projetos/py_rgb/.venv/bin/python3
from typing import TYPE_CHECKING

from openrgb.utils import DeviceType

if TYPE_CHECKING:
    from openrgb import OpenRGBClient
    from openrgb.orgb import Device
    from openrgb.utils import RGBColor


class Mobo:
    def __init__(self, mobo: Device) -> None:
        self.mobo = mobo
        self.mobo.set_mode("Static")

    def set_color(self, color: RGBColor) -> None:
        self.mobo.set_color(color)


class Ram:
    def __init__(self, ram: Device) -> None:
        self.ram = ram
        self.ram.set_mode("Static")

    def set_full_color(self, color: RGBColor) -> None:
        self.ram.set_color(color)

    def set_single_led_color(self, index: int, color: RGBColor) -> None:
        leds = self.ram.leds
        if index < 0 or index >= len(leds):
            raise IndexError("LED index out of range")  # noqa: EM101, TRY003
        leds[index].set_color(color)

    def set_dinamic_color(self, colors: list[RGBColor]) -> None:
        self.ram.set_colors(colors)


def get_rams(client: OpenRGBClient) -> list[Ram]:
    rams = client.get_devices_by_type(DeviceType.DRAM)
    if not rams:
        raise ValueError("No RAMs found")  # noqa: EM101, TRY003
    return [Ram(ram=ram) for ram in rams]


def get_mobo(client: OpenRGBClient) -> Mobo:
    mobo = client.get_devices_by_type(DeviceType.MOTHERBOARD)
    if not mobo:
        raise ValueError("No motherboard found")  # noqa: EM101, TRY003
    return Mobo(mobo=mobo[0])
