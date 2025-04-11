"""
--------------------------------------------------------------------------
Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2021-2025 - Allen Mikhailov

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

Button Driver

  This driver can support buttons that have either a pull up resistor between the
button and the processor pin (i.e. the input is "High" / "1" when the button is
not pressed) and will be connected to ground when the button is pressed (i.e. 
the input is "Low" / "0" when the button is pressed), or a pull down resistor 
between the button and the processor pin (i.e. the input is "Low" / "0" when the 
button is not pressed) and will be connected to power when the button is pressed
(i.e. the input is "High" / "1" when the button is pressed).

  To select the pull up configuration, press_low=True.  To select the pull down
configuration, press_low=False.


Software API:

  Button(pin, press_low)
    - Provide pin that the button monitors
    
    

"""
import time
from typing import Callable
import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH          = GPIO.HIGH
LOW           = GPIO.LOW

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Button():
    """ Button Class """
    pin: str
    
    # press_low: bool
    unpressed_value               = None
    pressed_value                 = None
    detection                     = None

    debug: bool
    
    sleep_time: float
    press_duration: float

    pressed_callback: Callable = lambda: None
    
    
    def __init__(self, pin: str, press_low: bool=True, sleep_time: float=0.1, debug: bool=True):
        """ Initialize variables and set up the button """
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin
        
        self.debug = debug

        # For pull up resistor configuration:    press_low = True
        # For pull down resistor configuration:  press_low = False
        if press_low:
            self.unpressed_value = HIGH
            self.pressed_value   = LOW
            self.detection       = GPIO.RISING
        else:
            self.unpressed_value = LOW
            self.pressed_value   = HIGH
            self.detection       = GPIO.FALLING
        
        # By default sleep time is "0.1" seconds
        self.sleep_time      = sleep_time
        self.press_duration  = 0.0        

        # Initialize the hardware components        
        self._setup()
    
    # End def

    def pressed(self):
        if (self.debug):
            print(f"Button {self.pin} pressed")
        self.pressed_callback()
        
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Button
        # HW#4 TODO: (one line of code)
        #   Remove "pass" and use the Adafruit_BBIO.GPIO library to set up the button
        print(f"Attempt pin setup {self.pin}")
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, self.detection, lambda a: self.pressed(), (int) (self.sleep_time*1000))
        pass

    # End def


    def is_pressed(self):
        """ Is the Button pressed?
        
           Returns:  True  - Button is pressed
                     False - Button is not pressed
        """
        # HW#4 TODO: (one line of code)
        #   Remove "pass" and return the comparison of input value of the GPIO pin of 
        #   the buton (i.e. self.pin) to the "pressed value" of the class 
        return GPIO.input(self.pin) == 0

    # End def


    
    def get_last_press_duration(self):
        """ Return the last press duration """
        return self.press_duration
    
    # End def
    
    
    def cleanup(self):
        """ Clean up the button hardware. """
        # Nothing to do for GPIO
        GPIO.remove_event_detect(self.pin)
    
    # End def
    
    
    # -----------------------------------------------------
    # Callback Functions
    # -----------------------------------------------------

    def set_pressed_callback(self, function: Callable):
        """ Function excuted every "sleep_time" while the button is pressed """
        self.pressed_callback = function
    
    # End def

    
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Button Test")

    # Create instantiation of the button
    button = Button("P2_2")
    
    # Create functions to test the callback functions
    def pressed():
        print("  Button pressed")
    # End def
    
    def unpressed():
        print("  Button not pressed")
    # End def

    def on_press():
        print("  On Button press")
        return 3
    # End def

    def on_release():
        print("  On Button release")
        return 4
    # End def    

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        # Check if the button is pressed
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))

        print("Press and hold the button.")
        time.sleep(4)
        
        # Check if the button is pressed
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))
        
        print("Release the button.")
        time.sleep(4)
   
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")

