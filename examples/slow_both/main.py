import time
import board
import busio

import lsm303

i2c = busio.I2C(board.SCL, board.SDA)
sensor = lsm303.LSM303(i2c)

while True:
	accel_x, accel_y, accel_z = sensor.accelerometer
	mag_x, mag_y, mag_z = sensor.magnetometer

	print('Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(accel_x, accel_y, accel_z))
	print('Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(mag_x, mag_y, mag_z))
	print('')
	time.sleep(1.0)
