# PowerSpec G478 RGB on Linux · Blue Breathing

![Blue Breathing concept art with a 43-inch Samsung M70H Mini LED TV showing a blue eclipse, blue LANCOOL 206 fan rings, and a translucent Redragon keyboard](blue-breathing-cover.jpg)

*Concept art inspired by the setup, with a 43-inch Samsung M70H Mini LED 4K TV.*

[Quick start](#quick-start) · [Troubleshooting](#troubleshooting) · [How I used Codex](#how-i-used-codex)

I wanted slow blue breathing across my setup, with no green and no Windows boot. This is what worked on my PowerSpec G478. The front fans and Zotac GPU are confirmed. The motherboard, keyboard, and mouse have the limits below.

## Quick start

Install Python 3 and [OpenRGB](https://openrgb.org/releases.html) for your distro. For the Zotac card, build [SpectraCtrl](https://github.com/Doodcom/SpectraCtrl) using its instructions and put the executable on your PATH or at `~/.local/bin/spectractl`. The script uses tools already installed. It does not install packages or start a background service.

```sh
python3 blue-breathing.py          # check what the controllers report
python3 blue-breathing.py --apply  # send blue breathing to the GPU and MSI board
```

The apply command exits with status 1 if either controller fails to report the requested mode or if the GPU fails to report blue. A successful exit does not verify the physical LEDs or synchronize their timing.

| Hardware | What worked |
| --- | --- |
| Zotac RTX 4080 SUPER Trinity Black | SpectraCtrl identified controller `N702E-1002`. The saved color was blue, but LED power was off. `spectractl on` restored it. `spectractl mode breathe 0000FF 100` set blue breathing, confirmed by `spectractl status`. |
| PowerSpec / LANCOOL 206 front fans | Tap **M** until the whole blue ring dims and brightens together. A moving pattern that travels inward or outward is a different preset. Tap **C** to cycle to blue. If the rings are linked, use the inner pair. Otherwise use each ring's own pair. |
| MSI MPG Z790 EDGE WIFI | Rainbow Wave brought the lights back. OpenRGB continued to report Rainbow Wave after a blue Breathing command, so blue breathing on this board is unverified. If a change makes the board go dark, the recovery that worked here was selecting that board in OpenRGB and applying **Rainbow wave** without brightness or speed flags. Use `openrgb --list-devices` to get the current device number first. |
| Redragon ELF PRO K649 | Connect the USB cable and move the side switch to **OFF** for wired mode. The official K649 app opened under Wine. I confirmed solid blue using **Fixed_on**, the dark-blue square, and Save. For blue breathing, choose **Respire**, select dark blue, clear **Colourful**, and save. Check the physical keys while idle. Blue breathing was not independently verified. |
| [Samsung M70H 43-inch Mini LED 4K TV](https://www.samsung.com/us/tvs/mini-led-tv/43-inch-mini-led-4k-tv-m70h-sku-un43m70hafxza/) | The display is part of the setup and the artwork. Its settings are outside the scope of the RGB script. |
| SteelSeries Aerox 3 Wireless | OpenRGB exposed **Rainbow Breathing**, which includes green. The script leaves the mouse alone. |

[PowerSpec case button guide](https://community.microcenter.com/discussion/14124/powerspec-atx-206-chassis) · [Redragon K649 software](https://redragonshop.com/pages/software)

## Troubleshooting

This guide is for a **PowerSpec G478 running Linux**. The goal is blue breathing: the LEDs stay blue and smoothly dim and brighten together. The LANCOOL 206 front fans, Zotac GPU, MSI motherboard, and Redragon keyboard each have their own lighting controller. Pick the section for the part you want to fix.

### How do I set PowerSpec G478 front fans to blue breathing?

The LANCOOL 206 case has two **M** buttons for lighting effects and two **C** buttons for colors. One pair controls the inner fan lights and the other controls the outer rings.

1. Tap **M** once at a time. Wait long enough to see whether the whole ring dims and brightens together. If the light travels inward or outward, keep cycling.
2. Tap **C** to select blue. If one pair changes both rings, use that pair. If the rings respond separately, repeat on the other pair.

This uses the case buttons and works without a Linux app. [PowerSpec case button guide](https://community.microcenter.com/discussion/14124/powerspec-atx-206-chassis)

### Why is my Zotac RTX 4080 SUPER RGB off on Linux?

On the **Zotac RTX 4080 SUPER Trinity Black** tested here, OpenRGB didn't list the card and its LEDs were dark. [SpectraCtrl](https://github.com/Doodcom/SpectraCtrl) could reach the GPU's lighting controller. Install it using the upstream instructions, then run:

```sh
spectractl status
spectractl on                       # if status shows power: off
spectractl mode breathe 0000FF 100
spectractl status
```

On this setup the final status showed **on**, **breathe**, and **#0000FF**. If the first command can't identify your lighting controller, check the model and support in SpectraCtrl before sending changes.

### What if the MSI motherboard lights go dark or stay on Rainbow Wave?

Run `openrgb --list-devices` and find the current number for **MSI MPG Z790 EDGE WIFI (MS-7D91)**. To recover the previously working effect, run `openrgb --device NUMBER --mode 'Rainbow wave'`, replacing `NUMBER` with that device number. This restored visible lighting on the tested board. Rainbow Wave includes green, and blue breathing on this board is still unverified.

### Why is my Redragon ELF PRO K649 preview blue but the keys only light when I type?

The physical keyboard is still running a reactive effect. Connect it with a USB data cable and slide the side switch to **OFF** for wired mode. Open the [Redragon K649 app](https://redragonshop.com/pages/software), which launched under Wine on this setup.

1. Click the **lightbulb icon**, select **Fixed_on**, then click the dark-blue square below the color wheel.
2. Click the **floppy-disk icon** to save. Look at the keyboard while idle. The physical keys should stay blue.
3. To try breathing, select **Respire**, choose dark blue again, clear **Colourful**, and save. Watch the physical keys while idle to check that they fade together.

Solid blue was confirmed on the keyboard here. Blue breathing was not independently verified.

## How I used Codex

I told Codex what I could see on the actual hardware. It checked which controllers Linux could see and read back the settings after each change. That mattered because an OpenRGB command could exit successfully while the MSI controller still reported the old effect, and the Redragon app could show a blue preview while the physical keys were still in Reaction mode.

Codex found the Linux tool that could reach my Zotac card, read back that its lighting power was off, and turned it on. I handled the case buttons and confirmed when the whole fan ring was fading together. Then I asked Codex to turn the working steps into one Linux script and write down the manual steps too.
