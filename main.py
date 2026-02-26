#! /usr/bin/uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "elevate>=0.1.3",
#     "nvidia-ml-py>=13.590.48",
# ]
# ///
import os

import pynvml
from elevate import elevate

SET_FAN_SPEED_PERCENTAGE = 50


def __nvml_main() -> None:
    devices_count = pynvml.nvmlDeviceGetCount()
    for device in range(devices_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(device)

        name = pynvml.nvmlDeviceGetName(handle)
        print(f"Processing {name!r}...")

        current_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        print(f"  Current temp is {current_temp!r}")

        fans_count = pynvml.nvmlDeviceGetNumFans(handle)
        print(f"  Fans count is {fans_count!r}")

        for fan in range(fans_count):
            current_speed = pynvml.nvmlDeviceGetFanSpeed_v2(handle, fan)
            print(f"  Current fan #{fan} is {current_speed}%")
            if current_speed == SET_FAN_SPEED_PERCENTAGE:
                continue

            print(f"  Setting fan #{fan} speed to {SET_FAN_SPEED_PERCENTAGE}%")
            pynvml.nvmlDeviceSetFanSpeed_v2(handle, fan, SET_FAN_SPEED_PERCENTAGE)


def __nvml_start() -> None:
    pynvml.nvmlInit()

    try:
        __nvml_main()
    finally:
        pynvml.nvmlShutdown()


def main() -> None:
    if os.getuid() != 0:
        elevate()

    __nvml_start()


if __name__ == "__main__":
    main()
