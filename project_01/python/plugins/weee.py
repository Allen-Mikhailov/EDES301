from plugin import Plugin, Action, Commander
from drivers.mpu6050.mpu6050 import MPU6050


class WeeeAction(Action):
	mpu6050: MPU6050
	def __init__(self, commander: Commander, mpu6050: MPU6050):
		super().__init__(commander, "WeeeAction", 5, 0)

		self.mpu6050 = mpu6050

	def loop(self):
		super().loop()

		ax, ay, az = self.mpu6050.get_acceleration()

		if (abs(ay) > 1):
			self.commander.state_machine.set_ready_state(self.name, True)


class WeeePlugin(Plugin):
	mpu6050: MPU6050
	def __init__(self, commander: Commander, mpu6050):
		super().__init__(commander, "WeeePlugin")

		self.mpu6050 = mpu6050

		weeeAction: WeeeAction = WeeeAction(commander, mpu6050)
		self.add_action(weeeAction)