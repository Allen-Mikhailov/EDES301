# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer
--------------------------------------------------------------------------
License:   
Copyright 2021-2025 Erik Welsh

Based on library from

Copyright 2018 Nicholas Lester

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
This file provides an interface to a PWM controllered buzzer.
  - Ex:  https://www.adafruit.com/product/1536


APIs:
  - Buzzer(pin)
    - play(frequency, length=1.0, stop=False)
      - Plays the frequency for the length of time

    - stop(length=0.0)
      - Stop the buzzer (will cause breaks between tones)
      
    - cleanup()
      - Stop the buzzer and clean up the PWM

"""
import time
import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

class Buzzer():
    pin       = None
    
    def __init__(self, pin):
        self.pin = pin
 
        # NOTE:  No other setup required
 
    # End def
    
    
    def play(self, frequency, length=1.0, stop=False):
        """ Plays the frequency for the length of time.
            frequency - Value in Hz or None for no tone
            length    - Time in seconds (default 1.0 seconds)
            stop      - Stop the buzzer (will cause breaks between tones)
        """
        if frequency is not None:
            PWM.start(self.pin, 50, frequency)
            # !!! FIX !!! 
            print("Playing {0}".format(frequency))
            # !!! FIX !!! 
            if length != None:
                time.sleep(length)
                self.stop()
        else:
            self.stop()
        
    # End def

    
    def stop(self, length=0.0):
        """ Stops the buzzer (will cause breaks between tones)
            length    - Time in seconds (default 0.0 seconds)
        """
        # !!! FIX !!! 
        print("Stopping the buzzer")
        PWM.stop(self.pin)

        time.sleep(length)
        
    # End def

    
    def cleanup(self):
        """Stops the buzzer and cleans up the PWM.
             *** This function must be called during hardware cleanup ***
        """
        self.stop()
        PWM.cleanup()
    # End def
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Buzzer Test")
    
    buzzer = Buzzer("P1_36")
    
    print("Play tone")
    
    buzzer.play(440, 1.0, False)      # Play 440Hz for 1 second
    time.sleep(1.0)
    buzzer.play(880, 1.0, True)       # Play 440Hz for 1 second
    time.sleep(1.0)   

    buzzer.cleanup()
    
    print("Test Complete")

