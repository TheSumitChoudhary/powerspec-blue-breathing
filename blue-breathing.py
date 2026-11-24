#!/usr/bin/env python3
"""Check or apply the PowerSpec G478 Blue Breathing preset on Linux."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

BLUE = "0000FF"
BOARD = "MSI MPG Z790 EDGE WIFI (MS-7D91)"
MOUSE = "SteelSeries Aerox 3 Wireless"
ZOTAC_CONTROLLER = "N702E-1002"


def run(*command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail or f"Exit status {result.returncode}")
    return result.stdout


def zotac(apply):
    executable = shutil.which("spectractl")
    if not executable:
        executable = Path.home() / ".local/bin/spectractl"
    status = run(executable, "status")
    if not re.search(rf"^controller:\s+{ZOTAC_CONTROLLER}\b", status, re.M):
        print("Zotac GPU: expected lighting controller not found.")
        return False
    if apply:
        run(executable, "mode", "breathe", BLUE, "100")
        status = run(executable, "status")
        if re.search(r"^power:\s+off\s*$", status, re.M):
            run(executable, "on")
            status = run(executable, "status")
    expected = {"power": "on", "mode": "breathe", "color": f"#{BLUE}"}
    values = dict(re.findall(r"^(power|mode|color):\s*(\S+)", status, re.M))
    print("Zotac GPU:", ", ".join(f"{key} {value}" for key, value in values.items()))
    return values == expected


def openrgb(apply):
    details = run("openrgb", "--list-detailed")
    devices = {}
    for section in re.split(r"(?m)(?=^\d+: )", details):
        heading = re.match(r"(\d+): (.+)", section)
        if heading:
            index, name = heading.groups()
            devices[name.strip()] = (index, section)

    print(f"SteelSeries mouse: {'detected' if MOUSE in devices else 'not detected'}.")
    print("OpenRGB exposes Rainbow Breathing for the mouse. The script leaves it alone.")
    if BOARD not in devices:
        print("MSI motherboard: not detected.")
        return False
    if apply:
        try:
            run("openrgb", "--device", devices[BOARD][0], "--mode", "Breathing",
                "--color", BLUE, "--speed", "35")
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
            print(f"MSI motherboard: {error}")
            return False
        return openrgb(False)
    active = re.search(r"(?m)^\s*Modes:.*?\[([^\]]+)\]", devices[BOARD][1])
    mode = active.group(1) if active else "unknown"
    print(f"MSI motherboard: reported mode {mode}. Verify color on the physical LEDs.")
    return mode.casefold() == "breathing"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="send the preset to the Zotac GPU and MSI board")
    args = parser.parse_args()
    if not sys.platform.startswith("linux"):
        parser.error("This script requires Linux.")

    verified = True
    for name, check in (("Zotac GPU", zotac), ("OpenRGB", openrgb)):
        try:
            verified = check(args.apply) and verified
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
            print(f"{name}: {error}")
            verified = False

    print("\nPowerSpec front fans: Tap M until the whole ring fades together. Tap C for blue.")
    print("Use the inner M/C pair if the rings are linked, or set each ring separately.")
    print("Redragon ELF PRO: In the K649 app, select Respire, click the dark-blue")
    print("square, clear Colourful, and click Save. Verify that the physical keys pulse.")
    print("The script cannot verify the front-fan, keyboard, or mouse lighting.")
    return 1 if args.apply and not verified else 0


if __name__ == "__main__":
    sys.exit(main())
