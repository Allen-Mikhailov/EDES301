import adafruit_mpu6050

from board import SCL, SDA, SCL_2, SDA_2
import busio
import time

class MPU6050:
	address: int 
	bus: int
	i2c = None
	mpu = None
	def __init__(self, address: int, bus: int) -> None:
		self.address = address
		self.bus = bus

		if bus == 1:
			self.i2c = busio.I2C(SCL, SDA)
		elif bus == 2:
			self.i2c = busio.I2C(SCL_2, SDA_2) # is defined on the pocket beagle
		else:
			raise ValueError(f"Invalid bus \"{bus}\"")
		
		self.mpu = adafruit_mpu6050.MPU6050(self.i2c)

	def get_acceleration(self):
		return self.mpu.acceleration
	
	def get_gyro(self):
		return self.mpu.gyro
	
	def get_temp(self):
		return self.mpu.temperature
	

if __name__ == '__main__':
	mpu = MPU6050(0x7d, 1)
	while True:
		print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.get_acceleration()))
		print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.get_gyro()))
		print("Temperature: %.2f C"%mpu.get_temp())
		print("")
		time.sleep(1)