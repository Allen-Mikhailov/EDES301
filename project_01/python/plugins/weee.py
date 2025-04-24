from plugin import Plugin, Action, Commander
from drivers.mpu6050.mpu6050 import MPU6050
from drivers.buzzer.buzzer import Buzzer
import math

gravity_constant = 10
wee_threshold = 0.80
raw_threshold = gravity_constant * wee_threshold

class WeeeAction(Action):
	mpu6050: MPU6050
    buzzer: Buzzer
    def __init__(self, commander: Commander, mpu6050: MPU6050, buzzer: Buzzer):
		super().__init__(commander, "WeeeAction", 5, 0)

		self.mpu6050 = mpu6050
        self.buzzer = buzzer

	def loop(self):
		super().loop()

		ax, ay, az = self.mpu6050.get_acceleration()
        magnitude = math.sqrt(ax*ax + ay*ay + az*az)

        should_be_ready: bool = magnitude < raw_threshold
        self.state_machine.set_ready_state(self.name, should_be_ready)

        if self.is_active:
            threshold_dif: float = raw_threshold-magnitude
            buzzer.play(440 + threshold_dif * 40)

    def release(self):
        super().release()
        buzzer.stop()
        

class WeeePlugin(Plugin):
	mpu6050: MPU6050
    buzzer: Buzzer
	def __init__(self, commander: Commander, mpu6050, buzzer: Buzzer):
		super().__init__(commander, "WeeePlugin")

		self.mpu6050 = mpu6050
        self.buzzer = buzzer

		weeeAction: WeeeAction = WeeeAction(commander, mpu6050)
		self.add_action(weeeAction)
