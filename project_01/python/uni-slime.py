"""
--------------------------------------------------------------------------
Uni-Slime
--------------------------------------------------------------------------
License:   
Copyright 2025 Allen Mikhailov

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Description

Requirements:
  -

Uses:
  -

"""
import time
from plugins.plugin import Plugin, Action, Commander
from typing import cast
from state_machine import StateMachine


import Adafruit_BBIO.GPIO as GPIO

# import plugins.simple_movement 
from plugins.home import HomePlugin

# import ht16k33 as HT16K33
from drivers.button.button import Button
from drivers.dpad.dpad import DPad
from drivers.oled_display.oled_display import OLEDDisplay
from drivers.mpu6050.mpu6050 import MPU6050

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class UniSlime(Commander):
	def __init__(self):
		pass

	def add_driver(self, name: str, driver):
		self.drivers[name] = driver

	def add_plugin(self, plugin: Plugin):
		self.plugins[plugin.name] = plugin
		for action in plugin.actions:
			self.add_action(action)


	def add_action(self, action: Action):
		# checking for name conflicts
		if action.name in self.actions:
			original_action = cast(Plugin, self.actions[action.name].parent_plugin).name
			plugin_name = cast(Plugin, action.parent_plugin).name
			raise ValueError(f"Action {action.name} name conflict between the plugins {plugin_name} and {original_action}")
		
		self.actions[action.name] = action

			

	def run(self):
		# loop infinitly
		while True:
			for action_name in self.actions:
				self.actions[action_name].loop()

			# dont know if this line will stay
			time.sleep(0.001) # sleep 1 ms

	def cleanup(self):
		pass



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

	print("Program Start")
	
	GPIO.cleanup()

	# Create instantiation of the people counter
	
	uni_slime = UniSlime()

	# adding drivers	
	dpad: DPad = DPad("P1_4", "P1_6", "P1_8", "P1_10", "P1_12")
	mouth_display = OLEDDisplay(1, 0x3c)
<<<<<<< HEAD
	home_button = Button("P1_2")
=======
	home_button = Button("P_02")
	mpu6050 = MPU6050(0x7d, 1)
>>>>>>> f2ee7a2426441e24b318d328ca1827295638ce2e

	uni_slime.add_driver("Dpad", dpad)
	uni_slime.add_driver("MouthOLED", mouth_display)
	uni_slime.add_driver("HomeButton", home_button)
	uni_slime.add_driver("mpu6050", mpu6050)
	

	# Adding plugins
	home_plugin = HomePlugin(uni_slime, mouth_display, dpad, home_button)

	uni_slime.add_plugin(home_plugin)

	try:
		# Run the people counter
		uni_slime.run()

	except KeyboardInterrupt:
		# Clean up hardware when exiting
		uni_slime.cleanup()

	print("Program Complete")

