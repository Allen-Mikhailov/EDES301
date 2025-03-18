"""
--------------------------------------------------------------------------
LED Driver
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

LED Driver

  This driver uses the flag "low_off" to determine if the LED is configured 
such that the LED is ON when the output is "High"/"1" and OFF when the output is 
"Low" / "0", i.e. "low_off=True", or that the LED is OF when the output is 
"High"/"1" and ON when the output is "Low" / "0", i.e. "low_off=False",

Software API:

  LED(pin, low_off=True)
    - Provide pin that the LED is connected
    
    is_on()
      - Return a boolean value (i.e. True/False) if the LED is ON / OFF

    on()
      - Turn the LED on

    off()
      - Turn the LED off    

"""
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

class LED():
    """ LED Class """
    pin             = None
    on_value        = None
    off_value       = None
    
    def __init__(self, pin=None, low_off=True):
        """ Initialize variables and set up the LED """
        if (pin == None):
            raise ValueError("Pin not provided for LED()")
        else:
            self.pin = pin
        
        # By default the "ON" value is "1" and the "OFF" value is "0".  
        # This is done to make it easier to change in the future
        if low_off:
            self.on_value  = HIGH
            self.off_value = LOW
        else:
            self.on_value  = LOW
            self.off_value = HIGH

        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize LED

        GPIO.setup(self.pin, GPIO.OUT);
        
        self.off()

    # End def


    def is_on(self):
        """ Is the LED on?
        
           Returns:  True  - LED is ON
                     False - LED is OFF
        """
        
        return GPIO.input(self.pin) == self.on_value

    # End def

    
    def on(self):
        """ Turn the LED ON """

        GPIO.output(self.pin, self.on_value)
    
    # End def
    
    
    def off(self):
        """ Turn the LED OFF """

        GPIO.output(self.pin, self.off_value)
    
    # End def


    def cleanup(self):
        """ Cleanup the hardware components. """
        # Turn LED off 
        self.off()
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    print("LED Test")

    # Create instantiation of the LED
    led = LED("P2_4")
    
    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    print("Use Ctrl-C to Exit")
    
    try:
        while(1):
            # Turn LED ON
            led.on()
            print("LED ON? {0}".format(led.is_on()))
            time.sleep(1)
            
            # Turn LED OFF
            led.off()
            print("LED ON? {0}".format(led.is_on()))
            time.sleep(1)
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")

