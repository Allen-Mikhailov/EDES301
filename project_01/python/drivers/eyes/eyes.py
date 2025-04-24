from __future__ import annotations
from enum import Enum

from board import SCL, SDA, SCL_2, SDA_2
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont  # Use Pillow for fonts
import math

fnt = ImageFont.load_default()

class Eyes():
    bus: int 
    addr: int 

    width: int 
    height: int

    display = None
	def __init__(self, bus: int, address: int, width: int=128, height:int=64) -> None:
        self.bus = bus
        self.addr = address

        self.width = width
        self.height = height

		if bus == 1:
			self.i2c = busio.I2C(SCL, SDA)
		elif bus == 2:
			self.i2c = busio.I2C(SCL_2, SDA_2) # is defined on the pocket beagle
		else:
			raise ValueError(f"Invalid bus \"{bus}\"")

		self.display = adafruit_ssd1306.SSD1306_I2C(width, height, self.i2c, addr=address)


        
