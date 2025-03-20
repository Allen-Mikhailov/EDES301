from __future__ import annotations
from enum import Enum

from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont  # Use Pillow for fonts


def draw_box(display, x, y, width, height, color):
	left: int  = x
	right: int = x + width - 1
	top: int   = y
	bot: int   = y + height - 1
	display.fill_rect(left, top, right, bot, color)

class ScreenMode(Enum):
	RAW = 0    # for directly using the display api
	SCREEN = 1 # for using the screen api

class ScreenElement():
	name: str = ""
	x: int = 0
	y: int = 0
	width: int = 10
	height: int = 10

	on_update: function | None
	on_select: function | None

	selected: bool = False


	def __init__(self, name) -> None:
		self.name = name

	def get_center(self) -> tuple[float, float]:
		return (self.x + self.width / 2.0, self.y + self.height / 2.0)

	def display(self, display):
		pass

	# overwrite if is selectable 
	def is_selectable(self) -> bool:
		return False
	
	def set_on_update(self, on_update: function):
		self.on_update = on_update

	def set_on_select(self, on_select: function):
		self.on_select = on_select

	def update(self):
		if self.on_update != None:
			self.on_update()

	def set_selected(self, selected: bool):
		self.selected = selected

	def toggle_selected(self):
		self.set_selected(not self.selected)
		

class ScreenBorder(ScreenElement):
	def display(self, display):
		super().display(display)

		left: int  = self.x
		right: int = self.x + self.width - 1
		top: int   = self.y
		bot: int   = self.y + self.height - 1
		
		display.line(left, top, right, top, 1)  # top
		display.line(left, bot, right, bot, 1)  # bottom
		display.line(left, top, left, bot, 1)   # left
		display.line(right, top, right, bot, 1) # right

TEXT_SIZE = 8
TEXT_PADDING = 2
	
class ScreenText(ScreenElement):
	text: str = ""
	font_color: int = 1
	def __init__(self, name) -> None:
		super().__init__(name)
		
	# text: str = ""
	def display(self, display):
		super().display(display)
		display.text(self.text, self.x+TEXT_PADDING, self.y+TEXT_PADDING, self.font_color)

	def set_text(self, text):
		self.text = text
		self.update()

	def set_font_color(self, font_color):
		self.font_color = font_color

class ScreenButton(ScreenText, ScreenBorder):
	def __init__(self, name) -> None:
		super().__init__(name)

	def display(self, display):
		if (self.selected):
			draw_box(display, self.x, self.y, self.width, self.height, 1)
			self.set_font_color(0)
			ScreenText.display(self, display)
		else:
			self.set_font_color(1)
			return super().display(display)
	
	def is_selectable(self) -> bool:
		return True
	
	def set_selected(self, selected: bool):
		super().set_selected(selected)
		self.update()
	


class Screen():
	selected_element: ScreenElement | None
	elements: dict[str, ScreenElement] = {}
	on_update: function | None
	def __init__(self) -> None:
		pass

	def add_element(self, element: ScreenElement):
		if element.name in self.elements:
			raise ValueError(f"Screen Element Name Conflict of name \"{element.name}\"")

		self.elements[element.name] = element

	def remove_element(self, element_name: str):
		del self.elements[element_name]

	def set_on_update(self, on_update: function | None):
		self.on_update = on_update

	def display_screen(self, display):
		# clear the display
		display.fill(0)

		# loop through all the elements and display them
		for element_name in self.elements:
			element: ScreenElement = self.elements[element_name]
			element.display(display)

		display.show()

	def move_dir(self, x, y):
		current_pos = ()

	def select(self):
		if (self.selected_element):
			self.selected_element.toggle_selected()




class OLEDDisplay():
	bus: int = 0
	address: int = 0
	i2c = None

	current_screen: Screen | None = None

	mode: ScreenMode = ScreenMode.RAW

	def __init__(self, bus: int, address: int) -> None:
		self.bus = bus
		self.address = address

		if bus == 1:
			self.i2c = busio.I2C(SCL, SDA)
		elif bus == 2:
			self.i2c = busio.I2C(SCL_2, SDA_2) # is defined on the pocket beagle
		else:
			raise ValueError(f"Invalid bus \"{bus}\"")

		
		self.display = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=address)

	def redraw(self):
		# Guard Clause
		if self.current_screen == None:
			return
		
		self.current_screen.display_screen(self.display)

	def release_screen(self):
		if self.current_screen != None:
			self.current_screen.set_on_update(None)
			self.current_screen = None

	def set_screen(self, screen: Screen):
		self.mode = ScreenMode.SCREEN

		self.release_screen()
		self.current_screen = screen
		screen.set_on_update(lambda: self.redraw())

		self.redraw()

	def set_mode_raw(self):
		self.release_screen()

		self.mode = ScreenMode.RAW

		self.display.fill(0)
		self.display.show()


if __name__ == '__main__':
	screen = Screen()
	button1 = ScreenButton("button1")
	button1.x = 0
	button1.y = 0
	button1.width = 100
	button1.height = 20
	button1.text = "BUT: 1"

	button2 = ScreenButton("button2")
	button2.x = 101
	button2.y = 21
	button2.width = 20
	button2.height = 40
	button1.text = "BUT: 2"

	screen.add_element(button1)
	screen.add_element(button2)

	display = OLEDDisplay(1, 0x3c)
	display.set_screen(screen)


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