from __future__ import annotations
from enum import Enum

from board import SCL, SDA, SCL_2, SDA_2
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont  # Use Pillow for fonts
import math

fnt = ImageFont.load_default()


def draw_box(draw: ImageDraw.ImageDraw, x, y, width, height, color):
	left: int  = x
	right: int = x + width - 1
	top: int   = y
	bot: int   = y + height - 1

	draw.rectangle((left, top, right, bot), fill=color)

class ScreenMode(Enum):
	RAW = 0    # for directly using the display api
	SCREEN = 1 # for using the screen api

class ScreenElement():
	name: str = ""
	x: int = 0
	y: int = 0
	width: int = 10
	height: int = 10

	on_update: function | None = None
	on_select: function | None = None
	on_press: function | None = None

	selected: bool = False


	def __init__(self, name) -> None:
		self.name = name

	def get_center(self) -> tuple[float, float]:
		return (self.x + self.width / 2.0, self.y + self.height / 2.0)

	def display(self, draw: ImageDraw.ImageDraw):
		pass

	# overwrite if is selectable 
	def is_selectable(self) -> bool:
		return False
	
	def set_on_update(self, on_update: function | None):
		self.on_update = on_update

	def set_on_pressed(self, on_press: function | None):
		self.on_press = on_press

	def set_on_select(self, on_select: function | None):
		self.on_select = on_select

	def update(self):
		if self.on_update != None:
			self.on_update()

	def set_selected(self, selected: bool):
		self.selected = selected

	def press(self):
		if self.on_press != None:
			self.on_press()


		

class ScreenBorder(ScreenElement):
	def display(self, draw: ImageDraw.ImageDraw):
		super().display(draw)

		left: int  = self.x
		right: int = self.x + self.width - 1
		top: int   = self.y
		bot: int   = self.y + self.height - 1
		
		draw.rectangle((left, top, right, bot), outline=255)
	
class ScreenText(ScreenElement):
	text: str = ""
	font_color: int = 255
	def __init__(self, name) -> None:
		super().__init__(name)
		
	# text: str = ""
	def display(self, draw: ImageDraw.ImageDraw):
		super().display(draw)
		center = self.get_center()

		bounds = self.get_text_bounds(draw)
		width = bounds[2]-bounds[0]
		height = bounds[3] - bounds[1]

		
		# we draw text at the center point - half the box
		draw.text((center[0]-width/2, center[1]-height/2), self.text, self.font_color)

	def set_text(self, text: str):
		self.text = text
		self.update()

	def get_text_bounds(self, draw: ImageDraw.ImageDraw):
		return draw.textbbox((0, 0), self.text)

	def set_font_color(self, font_color: int):
		self.font_color = font_color

class ScreenButton(ScreenText, ScreenBorder):
	def __init__(self, name) -> None:
		super().__init__(name)

	def display(self, draw: ImageDraw.ImageDraw):
		if (self.selected):
			draw_box(draw, self.x, self.y, self.width, self.height, 255)
			self.set_font_color(0)
			ScreenText.display(self, draw)
		else:
			self.set_font_color(255)
			return super().display(draw)
	
	def is_selectable(self) -> bool:
		return True
	
	def set_selected(self, selected: bool):
		super().set_selected(selected)
		self.update()
	


class Screen():
	selected_element: ScreenElement | None
	elements: dict[str, ScreenElement] = {}

	width: int = 0
	height: int = 0

	on_update: function | None = None

	image: Image.Image
	# draw: ImageDraw
	
	def __init__(self, width: int, height: int) -> None:
		self.width = width
		self.height = height
		self.image: Image.Image = Image.new("1", (width, height))
		self.draw = ImageDraw.Draw(self.image)

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
		draw_box(self.draw, 0, 0, self.width-1, self.height-1, 0)

		# loop through all the elements and display them
		for element_name in self.elements:
			element: ScreenElement = self.elements[element_name]
			element.display(self.draw)
		
		display.image(self.image)
		display.show()

	def move_dir(self, v: tuple[float, float]):
		# direction normalized
		dir = np.array(v) / np.hypot(v[0], v[1])

		# getting the current position
		current_pos: tuple[float, float] = (self.width/2, self.height/2)
		if (self.selected_element != None):
			current_pos = self.selected_element.get_center()

		# looping through all elements
		possible_selections = []
		for element_name in self.elements:
			element = self.elements[element_name]

			if (not element.is_selectable()):
				continue

			offset = np.array((element.x-current_pos[0],element.y-current_pos[1]))
			distance = np.hypot(offset[0], offset[1])

			# things too close can not be selected really
			if (distance < 5):
				continue

			offset_normalized = offset / distance
			dot = np.dot(dir, offset_normalized)

			# checking for greator than 45 deg diff
			if (dot < np.sqrt(2)/2):
				continue

			possible_selections.append((element, distance))

		if (len(possible_selections) > 0):
			# picking closest element
			possible_selections.sort(key=lambda x: x[1])
			selection: ScreenElement = possible_selections[0][0]

			# unselecting
			if (self.selected_element != None):
				self.selected_element.set_selected(False)
			

			# actually selecting
			selection.set_selected(True)
			self.selected_element = selection

		


	def press(self):
		if (self.selected_element):
			self.selected_element.press()




class OLEDDisplay():
	bus: int = 0
	address: int = 0
	i2c = None

	width: int
	height: int

	current_screen: Screen | None = None

	mode: ScreenMode = ScreenMode.RAW

	def __init__(self, bus: int, address: int, width: int=128, height:int=64) -> None:
		self.bus = bus
		self.address = address

		if bus == 1:
			self.i2c = busio.I2C(SCL, SDA)
		elif bus == 2:
			self.i2c = busio.I2C(SCL_2, SDA_2) # is defined on the pocket beagle
		else:
			raise ValueError(f"Invalid bus \"{bus}\"")

		self.width = width
		self.height = height
		
		self.display = adafruit_ssd1306.SSD1306_I2C(width, height, self.i2c, addr=address)

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
	screen = Screen(128, 64)
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
	button2.text = "BUT: 2"

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