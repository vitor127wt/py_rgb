#!/home/vueko/Projetos/py_rgb/.venv/bin/python3
import time
from typing import TYPE_CHECKING

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

from core import get_devices, get_info
from core.color_picker import Colors

if TYPE_CHECKING:
    from collections.abc import Callable

CLIENT = OpenRGBClient()

CPU_TEMP_RANGE = {
    "min": 35.0,
    "max": 95.0,
}
GPU_TEMP_RANGE = {
    "min": 30.0,
    "max": 90.0,
}


def generate_load_based_ram_colors(color: Colors) -> Callable[[float], list[RGBColor]]:
    color_list_raw = Colors.gradient(Colors.white.value, color.value, 6)

    color_list = [
        RGBColor.fromHEX(color_hex.get_hex_l()) for color_hex in color_list_raw
    ]

    def wrapper(load: float) -> list[RGBColor]:
        min_color = color_list[0]
        max_color = color_list[-1]

        full_leds_count = int(load // 12.5)
        rest_leds_count = load % 12.5
        trasition_led_color_index = min(int(rest_leds_count // 2), len(color_list) - 1)
        trasition_led_color = color_list[trasition_led_color_index]

        leds_state: list[RGBColor] = []

        for i in range(8):
            if i < full_leds_count:
                leds_state.append(max_color)
            elif i == full_leds_count and rest_leds_count >= 2:
                leds_state.append(trasition_led_color)
            else:
                leds_state.append(min_color)
        leds_state.reverse()
        return leds_state

    return wrapper


def get_temp_color(temp_raw: float) -> RGBColor:
    colors = [
        RGBColor.fromHEX(color.get_hex_l())
        for color in Colors.gradient(Colors.cian.value, Colors.purple.value, 16)
    ] + [
        RGBColor.fromHEX(color.get_hex_l())
        for color in Colors.gradient(Colors.purple.value, Colors.red.value, 16)
    ]

    temp = max(CPU_TEMP_RANGE["min"], min(GPU_TEMP_RANGE["max"], temp_raw))

    color_state = (temp - CPU_TEMP_RANGE["min"]) / (
        GPU_TEMP_RANGE["max"] - CPU_TEMP_RANGE["min"]
    )

    color_index = min(int(color_state * 32), len(colors))

    return colors[color_index]


cpu_ram_color = generate_load_based_ram_colors(Colors.orange)
gpu_ram_color = generate_load_based_ram_colors(Colors.green)

mobo = get_devices.get_mobo(client=CLIENT)
ram_1, ram_2 = get_devices.get_rams(client=CLIENT)


def mode() -> None:
    while True:
        time.sleep(1 / 60)
        try:
            cpu, gpu = get_info.get_info()
            mobo.set_color(get_temp_color(cpu.temp))
            ram_1.set_dinamic_color(cpu_ram_color(cpu.load))
            ram_2.set_dinamic_color(gpu_ram_color(gpu.load * 100))
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    mode()
