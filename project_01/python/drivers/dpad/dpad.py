# This driver used the button drivers to create the controls for a dpad

from button.button import Button
from typing import Callable

empty_func = lambda: None

class DPad():
	left_button: Button
	up_button: Button
	right_button: Button  
	down_button: Button  
	enter_button: Button

	on_enter: Callable
	on_move: Callable

	def __init__(self, left_pin, up_pin, right_pin, down_pin, enter_pin) -> None:
		self.left_button = Button(left_pin)
		self.up_button = Button(up_pin)
		self.right_button = Button(right_pin)
		self.down_button = Button(down_pin)
		self.enter_button = Button(enter_pin)

		self.on_move = empty_func
		self.on_enter = empty_func

		self.left_button.set_pressed_callback( lambda: self.on_move((-1, 0)))
		self.up_button.set_pressed_callback(   lambda: self.on_move((0, -1)))
		self.right_button.set_pressed_callback(lambda: self.on_move((1, 0)))
		self.down_button.set_pressed_callback( lambda: self.on_move((0, 1)))

		self.enter_button.set_pressed_callback(lambda: self.on_enter())

	def set_on_move(self, on_move: Callable | None):
		if on_move == None:
			self.on_move = empty_func
		else:
			self.on_move = on_move

	def set_on_enter(self, on_enter: Callable | None):
		if on_enter == None:
			self.on_enter = empty_func
		else:
			self.on_enter = on_enter

