import Adafruit_BBIO.GPIO as GPIO

class L293DNE:
    m1_left: str
    m1_right: str
    m2_left: str
    m2_right: str

    def __init__(self, m1_left: str, m1_right: str, m2_left: str, m2_right: str):
        self.m1_left  = m1_left
        self.m1_right = m1_right
        self.m2_left  = m2_left
        self.m2_right = m2_right

        GPIO.setup(m1_left, GPIO.OUT)
        GPIO.setup(m1_right, GPIO.OUT)
        GPIO.setup(m2_left, GPIO.OUT)
        GPIO.setup(m2_right, GPIO.OUT)

    def reset(self):
        GPIO.output(self.m1_left, GPIO.LOW)
        GPIO.output(self.m1_right, GPIO.LOW)
        GPIO.output(self.m2_left, GPIO.LOW)
        GPIO.output(self.m2_right, GPIO.LOW)
        
    def move_m1(self, direction: int):
        left: int = 0
        right: int = 0

        if direction == 1:
            right = 1
        elif direction == -1:
            left = 1

        GPIO.output(self.m1_left, left)
        GPIO.output(self.m1_right, right)
    
if __name__ == "__main__":
    driver = L293DNE("P2_29", "P2_31", "P2_33", "P2_35")
    driver.move_m1(1)
