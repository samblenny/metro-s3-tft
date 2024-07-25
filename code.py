# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# metro-s3-tft
#
# Hardware:
# - Adafruit Metro ESP32-S3 with 16 MB Flash 8 MB PSRAM
# - Adafruit 2.8" TFT Touch Shield for Arduino with Resistive Touch Screen v2
#
# TFT Touch Shield:
# - resolution: 240x320 px
# - TSC2007 touchscreen driver, ILI9341 display driver
# - TFT SPI: ICSP header = board.SPI()
# - TFT CS: #10 = board.D10
# - TFT DC: #9 = board.D9
#
from board import NEOPIXEL, D9, D10, SPI
from digitalio import DigitalInOut, Direction
from displayio import Bitmap, Group, Palette, TileGrid, release_displays
from fourwire import FourWire
from gc import collect, mem_free
from neopixel_write import neopixel_write
from time import sleep

from adafruit_ili9341 import ILI9341


def gcCol():
    # Collect garbage and print free memory
    collect()
    print('mem_free', mem_free())

def countdown(n):
    # Print a countdown to the console
    assert n > 1, "countdown argument is too small"
    for i in range(n, 0, -1):
        print(i)
        sleep(1)

def main():
    # Turn off neopixel
    np = DigitalInOut(NEOPIXEL)
    neopixel_write(np, bytearray([0,0,0]))
    # Initialize 2.8" TFT display shield
    release_displays()
    gcCol()
    bmp = Bitmap(320, 240, 1)
    pal = Palette(1)
    bus = FourWire(SPI(), command=D9, chip_select=D10)
    display = ILI9341(bus, width=320, height=240)
    display.rotation = 180  # landscape with Metro S3 USB port on the right
    gcCol()
    # Print a countdown while display is still in console mode
    countdown(5)
    # Switch to graphics mode and fill screen with a solid color
    grp1 = Group()
    display.root_group = grp1
    pal[0] = 0xAA00AA
    sprite = TileGrid(bmp, pixel_shader=pal, x=0, y=0)
    grp1.append(sprite)
    # EVENT LOOP
    while True:
        sleep(0.1)
        pass

main()
