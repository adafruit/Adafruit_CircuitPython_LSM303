# The MIT License (MIT)
#
# Copyright (c) 2017 Dave Astels for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_lsm303`
====================================================


CircuitPython driver for the LSM303 accelerometer.

* Author(s): Dave Astels
"""

# imports

try:
    import struct
except ImportError:
	import ustruct as struct
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/dastels/Adafruit_CircuitPython_lsm303.git"

# Internal constants and register values:
# pylint: disable=bad-whitespace
LSM303_ADDRESS_ACCEL	  = const(0x19) #	 (0x32 >> 1)		 // 0011001x
LSM303_ADDRESS_MAG		  = const(0x1E) #	 (0x3C >> 1)		 // 0011110x
LSM303_ID				  = const(0xD4) #	 (0b11010100)

REG_ACCEL_CTRL_REG1_A	  = const(0x20)
REG_ACCEL_CTRL_REG2_A	  = const(0x21)
REG_ACCEL_CTRL_REG3_A	  = const(0x22)
REG_ACCEL_CTRL_REG4_A	  = const(0x23)
REG_ACCEL_CTRL_REG5_A	  = const(0x24)
REG_ACCEL_CTRL_REG6_A	  = const(0x25)
REG_ACCEL_REFERENCE_A	  = const(0x26)
REG_ACCEL_STATUS_REG_A	  = const(0x27)
REG_ACCEL_OUT_X_L_A		  = const(0x28)
REG_ACCEL_OUT_X_H_A		  = const(0x29)
REG_ACCEL_OUT_Y_L_A		  = const(0x2A)
REG_ACCEL_OUT_Y_H_A		  = const(0x2B)
REG_ACCEL_OUT_Z_L_A		  = const(0x2C)
REG_ACCEL_OUT_Z_H_A		  = const(0x2D)
REG_ACCEL_FIFO_CTRL_REG_A = const(0x2E)
REG_ACCEL_FIFO_SRC_REG_A  = const(0x2F)
REG_ACCEL_INT1_CFG_A	  = const(0x30)
REG_ACCEL_INT1_SOURCE_A	  = const(0x31)
REG_ACCEL_INT1_THS_A	  = const(0x32)
REG_ACCEL_INT1_DURATION_A = const(0x33)
REG_ACCEL_INT2_CFG_A	  = const(0x34)
REG_ACCEL_INT2_SOURCE_A	  = const(0x35)
REG_ACCEL_INT2_THS_A	  = const(0x36)
REG_ACCEL_INT2_DURATION_A = const(0x37)
REG_ACCEL_CLICK_CFG_A	  = const(0x38)
REG_ACCEL_CLICK_SRC_A	  = const(0x39)
REG_ACCEL_CLICK_THS_A	  = const(0x3A)
REG_ACCEL_TIME_LIMIT_A	  = const(0x3B)
REG_ACCEL_TIME_LATENCY_A  = const(0x3C)
REG_ACCEL_TIME_WINDOW_A	  = const(0x3D)

REG_MAG_CRA_REG_M		  = const(0x00)
REG_MAG_CRB_REG_M		  = const(0x01)
REG_MAG_MR_REG_M		  = const(0x02)
REG_MAG_OUT_X_H_M		  = const(0x03)
REG_MAG_OUT_X_L_M		  = const(0x04)
REG_MAG_OUT_Z_H_M		  = const(0x05)
REG_MAG_OUT_Z_L_M		  = const(0x06)
REG_MAG_OUT_Y_H_M		  = const(0x07)
REG_MAG_OUT_Y_L_M		  = const(0x08)
REG_MAG_SR_REG_Mg		  = const(0x09)
REG_MAG_IRA_REG_M		  = const(0x0A)
REG_MAG_IRB_REG_M		  = const(0x0B)
REG_MAG_IRC_REG_M		  = const(0x0C)
REG_MAG_TEMP_OUT_H_M	  = const(0x31)
REG_MAG_TEMP_OUT_L_M	  = const(0x32)

MAGGAIN_1_3				  = const(0x20)	 # +/- 1.3 
MAGGAIN_1_9				  = const(0x40)	 # +/- 1.9
MAGGAIN_2_5				  = const(0x60)	 # +/- 2.5
MAGGAIN_4_0				  = const(0x80)	 # +/- 4.0
MAGGAIN_4_7				  = const(0xA0)	 # +/- 4.7
MAGGAIN_5_6				  = const(0xC0)	 # +/- 5.6
MAGGAIN_8_1				  = const(0xE0)	 # +/- 8.1

_ACCELTYPE				  = True
_MAGTYPE				  = False

class LSM303:
	"""Driver base for the LSM303 accelerometer."""

	# Class-level buffer for reading and writing data with the sensor.
	# This reduces memory allocations but means the code is not re-entrant or
	# thread safe!
	_BUFFER = bytearray(6)
	
	def __init__(self, i2c):
		self._accel_device = I2CDevice(i2c, LSM303_ADDRESS_ACCEL)
		self._mag_device = I2CDevice(i2c, LSM303_ADDRESS_MAG)
		# Enable the accelerometer
		self._write_u8(_ACCELTYPE, REG_ACCEL_CTRL_REG1_A, 0x27)
		# Enable the magnetometer
		self._write_u8(_MAGTYPE, REG_MAG_MR_REG_M, 0x00);


	def read(self):
		"""Read the raw accelerometer and magnetometer sensor values and return 
		it as a pair of 3-tuple of X, Y, Z axis values that are 16-bit unsigned values.
		"""
		self._read_bytes(_ACCELTYPE, REG_ACCEL_OUT_X_L_A | 0x80, 6, self._BUFFER)
		accel_x, accel_y, accel_z = struct.unpack_from('<hhh', self._BUFFER[0:6])

		self._read_bytes(_MAGTYPE, REG_MAG_OUT_X_H_M, 6, self._BUFFER)
		mag_x, mag_y, mag_z = struct.unpack_from('>hhh', self._BUFFER[0:6])
		return (accel_x, accel_y, accel_z, mag_x, mag_y, mag_z)


	def set_mag_gain(gain):
		write_u8(_MAGTYPE, REG_MAG_CRB_REG_M, gain)


	def _read_u8(self, sensor_type, address):
		if sensor_type == _ACCELTYPE:
			device = self._accel_device
		else:
			device = self._mag_device
		with device as i2c:
			self._BUFFER[0] = address & 0xFF
			i2c.write(self._BUFFER, end=1, stop=False)
			i2c.readinto(self._BUFFER, end=1)
		return self._BUFFER[0]


	def _read_bytes(self, sensor_type, address, count, buf):
		if sensor_type == _ACCELTYPE:
			device = self._accel_device
		else:
			device = self._mag_device
		with device as i2c:
			buf[0] = address & 0xFF
			i2c.write(buf, end=1, stop=False)
			i2c.readinto(buf, end=count)


	def _write_u8(self, sensor_type, address, val):
		if sensor_type == _ACCELTYPE:
			device = self._accel_device
		else:
			device = self._mag_device
		with device as i2c:
			self._BUFFER[0] = address & 0xFF
			self._BUFFER[1] = val & 0xFF
			i2c.write(self._BUFFER, end=2)
