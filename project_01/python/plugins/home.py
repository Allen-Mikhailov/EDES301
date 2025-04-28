# This plugin uses the home button a dpad to create a common home interface UI using the mouth screen

from plugin import Plugin, Action, Commander
from drivers.button.button import Button
from drivers.dpad.dpad import DPad
from drivers.oled_display.oled_display import OLEDDisplay, Screen, ScreenButton, ScreenText

class HomeAction(Action):
	# drivers
	dpad: DPad
	display: OLEDDisplay
	home_button: Button

	# Screens
	current_screen: Screen | None
	home_screen: Screen

	# UI

	def __init__(self, commander: Commander, display: OLEDDisplay, dpad: DPad, home_button: Button):
		super().__init__(commander, "HomeAction", 100, 0)

		self.display = display
		self.dpad = dpad
		self.home_button = home_button
		
		self.current_screen = None

		home_screen: Screen = Screen(display.width, display.height)
		self.home_screen = home_screen

		screen_title: ScreenText = ScreenText("HomeScreen-Title")
		screen_title.set_text("Title")
		home_screen.add_element(screen_title)

		# centering title
		title_bounds = screen_title.get_text_bounds(home_screen.draw)
		title_width = title_bounds[2] - title_bounds[0]
		screen_title.x = int(display.width/2 - title_width / 2)
		
		test_button_1 = ScreenButton("TestButton 1")
		test_button_1.set_text("Button 1")
		
		test_button_2 = ScreenButton("TestButton 2")
		test_button_2.set_text("Button 2")
		
		test_button_1.x = 80
		test_button_1.y = 10
		
		test_button_2.x = 80
		test_button_2.y = 40
		
		home_screen.add_element(test_button_1)
		home_screen.add_element(test_button_2)

		self.dpad.set_on_move(lambda _dir: None if self.current_screen == None else self.current_screen.move_dir(_dir))

		display.set_screen(home_screen)

	def toggle(self):
		if (self.commander != None):
			return

		self.commander.state_machine.set_ready_state(not self.is_ready)



class HomePlugin(Plugin):
	dpad: DPad
	display: OLEDDisplay
	home_button: Button

	home_action: HomeAction

	def __init__(self, commander: Commander, display: OLEDDisplay, dpad: DPad, home_button: Button):
		super().__init__(commander, "HomePlugin")

		self.display = display
		self.dpad = dpad
		self.home_button = home_button

		self.home_action = HomeAction(commander, display, dpad, home_button)

		home_button.set_pressed_callback(lambda: self.home_action.toggle())