#!/home/vueko/Projetos/py_rgb/.venv/bin/python3
from dataclasses import dataclass

import GPUtil
import psutil


@dataclass
class Cpu:
    temp: float
    load: float


@dataclass
class Gpu:
    temp: float
    load: float


def get_info() -> tuple[Cpu, Gpu]:
    # Get CPU temperature
    cpu_temp = psutil.sensors_temperatures().get("k10temp")
    if cpu_temp:
        cpu_info: Cpu = Cpu(
            temp=cpu_temp[0].current, load=psutil.cpu_percent(interval=0.1)
        )
    # Get GPU temperature
    gpus = GPUtil.getGPUs()[0]
    if gpus:
        gpu_info: Gpu = Gpu(temp=gpus.temperature, load=gpus.load)  # type: ignore

    return (cpu_info, gpu_info)  # type: ignore
