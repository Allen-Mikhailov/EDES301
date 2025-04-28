import board
import busio

# Import the SSD1306 module.
import adafruit_ssd1306

import inspect

i2c1 = busio.I2C(board.SCL, board.SDA)
i2c2 = busio.I2C(board.SCL_2, board.SDA_2)

display1 = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c1, addr=0x3c)
display2 = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c2, addr=0x3c)
# Alternatively you can change the I2C address of the device with an addr parameter:
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

def test_screen(display):
		# Clear the display.  Always call show after changing pixels to make the display
	# update visible!
	display.fill(0)

	display.show()

	# Set a pixel in the origin 0,0 position.
	display.pixel(0, 0, 1)
	# Set a pixel in the middle 64, 16 position.
	display.pixel(64, 16, 1)
	# Set a pixel in the opposite 127, 31 position.
	display.pixel(127, 31, 1)
	display.show()

test_screen(display1)
test_screen(display2)

for method in inspect.getmembers(display1, predicate=inspect.ismethod):
	print(method[0])