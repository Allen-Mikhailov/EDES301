"""
--------------------------------------------------------------------------
People Counter
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

Use the HT16K33 Display and a button to create a digital people counter

Requirements:
  - Increment the counter by one each time the button is pressed
  - If button is held for more than 2s, reset the counter

Uses:
  - HT16K33 display library developed in class

"""
import time

import ht16k33 as HT16K33
import button as BUTTON


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

class PeopleCounter():
    """ People Counter """
    reset_time = None
    button     = None
    display    = None
    
    def __init__(self, reset_time=2.0, button="P2_2", i2c_bus=1, i2c_address=0x70):
        """ Initialize variables and set up display """
        self.reset_time = reset_time
        self.button     = BUTTON.Button(button)
        self.display    = HT16K33.HT16K33(i2c_bus, i2c_address)
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Display
        
        self.display.update(0)
        

        print("People Counter setup()")

    # End def


    def run(self):
        """Execute the main program."""
        people_count                 = 0        # Number of people to be displayed
        button_press_time            = 0.0      # Time button was pressed (in seconds)
        
        while(1):
            self.button.wait_for_press()
            button_press_time = self.button.get_last_press_duration()
            
            if (button_press_time >= self.reset_time):
                people_count = 0
            else:
                people_count += 1
            
            if (people_count > HT16K33.HT16K33_MAX_VALUE):
                self.display.text("BIG")
            else:
                self.display.update(people_count)
    
            # Wait for button press / release

            # Get the press time

            # Compare time to increment or reset people_count

            # Update the display

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something unique to show program is complete
        self.display.text("DEAD")
        
        # Button does not need any cleanup code
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the people counter
    
    people_counter = PeopleCounter()

    try:
        # Run the people counter
        people_counter.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        people_counter.cleanup()

    print("Program Complete")

