from enum import Enum

from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

class OLEDDisplay():
	bus: int = 0
	address: int = 0
	i2c = None
	display = None

	mode = ""

	def __init__(self, bus: int, address: int) -> None:
		self.bus = bus
		self.address = address

		if bus == 1:
			self.i2c = busio.I2C(SCL, SDA)
		elif bus == 2:
			self.i2c = busio.I2C(SCL_2, SDA_2)
		else:
			raise ValueError(f"Invalid bus \"{bus}\"")

		
		self.display = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, address)


# i2c = busio.I2C(SCL, SDA)

# display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# # Clear the display.  Always call show after changing pixels to make the display
# # update visible!
# display.fill(0)

# display.show()

# # Set a pixel in the origin 0,0 position.
# display.pixel(0, 0, 1)
# # Set a pixel in the middle 64, 16 position.
# display.pixel(64, 16, 1)
# # Set a pixel in the opposite 127, 31 position.
# display.pixel(127, 31, 1)
# display.show()