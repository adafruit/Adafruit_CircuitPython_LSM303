import time
import board
import busio

import adafruit_lsm303

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm303.LSM303(i2c)

while True:
	accel_x, accel_y, accel_z = sensor.read_accel()
	mag_x, mag_y, mag_z = sensor.read_mag()

	print('Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(accel_x, accel_y, accel_z))
	print('Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(mag_x, mag_y, mag_z))
	print('')
	time.sleep(1.0)
