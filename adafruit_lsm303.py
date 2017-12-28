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
_ADDRESS_ACCEL             = const(0x19)  # (0x32 >> 1)       // 0011001x
_ADDRESS_MAG               = const(0x1E)  # (0x3C >> 1)       // 0011110x
_ID                        = const(0xD4)  # (0b11010100)

# Accelerometer registers
_REG_ACCEL_CTRL_REG1_A     = const(0x20)
_REG_ACCEL_CTRL_REG2_A     = const(0x21)
_REG_ACCEL_CTRL_REG3_A     = const(0x22)
_REG_ACCEL_CTRL_REG4_A     = const(0x23)
_REG_ACCEL_CTRL_REG5_A     = const(0x24)
_REG_ACCEL_CTRL_REG6_A     = const(0x25)
_REG_ACCEL_REFERENCE_A     = const(0x26)
_REG_ACCEL_STATUS_REG_A    = const(0x27)
_REG_ACCEL_OUT_X_L_A       = const(0x28)
_REG_ACCEL_OUT_X_H_A       = const(0x29)
_REG_ACCEL_OUT_Y_L_A       = const(0x2A)
_REG_ACCEL_OUT_Y_H_A       = const(0x2B)
_REG_ACCEL_OUT_Z_L_A       = const(0x2C)
_REG_ACCEL_OUT_Z_H_A       = const(0x2D)
_REG_ACCEL_FIFO_CTRL_REG_A = const(0x2E)
_REG_ACCEL_FIFO_SRC_REG_A  = const(0x2F)
_REG_ACCEL_INT1_CFG_A      = const(0x30)
_REG_ACCEL_INT1_SOURCE_A   = const(0x31)
_REG_ACCEL_INT1_THS_A      = const(0x32)
_REG_ACCEL_INT1_DURATION_A = const(0x33)
_REG_ACCEL_INT2_CFG_A      = const(0x34)
_REG_ACCEL_INT2_SOURCE_A   = const(0x35)
_REG_ACCEL_INT2_THS_A      = const(0x36)
_REG_ACCEL_INT2_DURATION_A = const(0x37)
_REG_ACCEL_CLICK_CFG_A     = const(0x38)
_REG_ACCEL_CLICK_SRC_A     = const(0x39)
_REG_ACCEL_CLICK_THS_A     = const(0x3A)
_REG_ACCEL_TIME_LIMIT_A    = const(0x3B)
_REG_ACCEL_TIME_LATENCY_A  = const(0x3C)
_REG_ACCEL_TIME_WINDOW_A   = const(0x3D)

# Magnetometer registers
_REG_MAG_CRA_REG_M         = const(0x00)
_REG_MAG_CRB_REG_M         = const(0x01)
_REG_MAG_MR_REG_M          = const(0x02)
_REG_MAG_OUT_X_H_M         = const(0x03)
_REG_MAG_OUT_X_L_M         = const(0x04)
_REG_MAG_OUT_Z_H_M         = const(0x05)
_REG_MAG_OUT_Z_L_M         = const(0x06)
_REG_MAG_OUT_Y_H_M         = const(0x07)
_REG_MAG_OUT_Y_L_M         = const(0x08)
_REG_MAG_SR_REG_Mg         = const(0x09)
_REG_MAG_IRA_REG_M         = const(0x0A)
_REG_MAG_IRB_REG_M         = const(0x0B)
_REG_MAG_IRC_REG_M         = const(0x0C)
_REG_MAG_TEMP_OUT_H_M      = const(0x31)
_REG_MAG_TEMP_OUT_L_M      = const(0x32)

# Magnetometer gains
MAGGAIN_1_3                = const(0x20)  # +/- 1.3 
MAGGAIN_1_9                = const(0x40)  # +/- 1.9
MAGGAIN_2_5                = const(0x60)  # +/- 2.5
MAGGAIN_4_0                = const(0x80)  # +/- 4.0
MAGGAIN_4_7                = const(0xA0)  # +/- 4.7
MAGGAIN_5_6                = const(0xC0)  # +/- 5.6
MAGGAIN_8_1                = const(0xE0)  # +/- 8.1

# Magentometer rates
MAGRATE_0_7                = const(0x00)  # 0.75 Hz
MAGRATE_1_5                = const(0x01)  # 1.5 Hz
MAGRATE_3_0                = const(0x62)  # 3.0 Hz
MAGRATE_7_5                = const(0x03)  # 7.5 Hz
MAGRATE_15                 = const(0x04)  # 15 Hz
MAGRATE_30                 = const(0x05)  # 30 Hz
MAGRATE_75                 = const(0x06)  # 75 Hz
MAGRATE_220                = const(0x07)  # 200 Hz

# Sensor types
_ACCELTYPE                 = True
_MAGTYPE                   = False

# Conversion constants
_LSM303ACCEL_MG_LSB        = 16704.0        # 1, 2, 4 or 12 mg per lsb
_LSM303MAG_GAUSS_LSB_XY    = 1100.0       # Varies with gain
_LSM303MAG_GAUSS_LSB_Z     = 980.0        # Varies with gain

_GRAVITY_STANDARD          = 9.80665      # Earth's gravity in m/s^2
_GAUSS_TO_MICROTESLA       = 100.0          # Gauss to micro-Tesla multiplier

class LSM303:
    """Driver for the LSM303 accelerometer/magnetometer."""

    # Class-level buffer for reading and writing data with the sensor.
    # This reduces memory allocations but means the code is not re-entrant or
    # thread safe!
    _BUFFER = bytearray(6)
    
    def __init__(self, i2c):
        self._accel_device = I2CDevice(i2c, _ADDRESS_ACCEL)
        self._mag_device = I2CDevice(i2c, _ADDRESS_MAG)
        self._write_u8(_ACCELTYPE, _REG_ACCEL_CTRL_REG1_A, 0x27) # Enable the accelerometer
        self._write_u8(_MAGTYPE, _REG_MAG_MR_REG_M, 0x00);       # Enable the magnetometer
        _mag_gain = 0
        self.set_mag_gain(MAGGAIN_1_3)


    def read_raw_accel(self):
        """Read the raw accelerometer sensor values and return 
        it as a 3-tuple of X, Y, Z axis values that are 16-bit signed integers.
        """
        self._read_bytes(_ACCELTYPE, _REG_ACCEL_OUT_X_L_A | 0x80, 6, self._BUFFER)
        return struct.unpack_from('<hhh', self._BUFFER[0:6])

    def read_accel(self):
        """Read the processed accelerometer sensor values and return 
        it as a 3-tuple of X, Y, Z axis values in meters per second squared that are signed floats.
        """
        raw_accel_data = self.read_raw_accel()
        return map(lambda n:n / _LSM303ACCEL_MG_LSB * _GRAVITY_STANDARD, raw_accel_data)


    def read_raw_mag(self):
        """Read the raw magnetometer sensor values and return 
        it as a 3-tuple of X, Y, Z axis values that are 16-bit signed integers.
        """
        self._read_bytes(_MAGTYPE, _REG_MAG_OUT_X_H_M, 6, self._BUFFER)
        return map(lambda n: n >> 4, struct.unpack_from('>hhh', self._BUFFER[0:6]))


    def read_mag(self):
        """Read the processed magnetometer sensor values and return 
        it as a 3-tuple of X, Y, Z axis values in microteslas that are signed floats.
        """
        mag_x, mag_y, mag_z = self.read_raw_mag()
        print(mag_x)
        print(mag_x / _LSM303MAG_GAUSS_LSB_XY)
        print(mag_x / _LSM303MAG_GAUSS_LSB_XY * _GAUSS_TO_MICROTESLA)
        
        return (mag_x / _LSM303MAG_GAUSS_LSB_XY * _GAUSS_TO_MICROTESLA,
                mag_y / _LSM303MAG_GAUSS_LSB_XY * _GAUSS_TO_MICROTESLA,
                mag_z / _LSM303MAG_GAUSS_LSB_Z * _GAUSS_TO_MICROTESLA)


    def set_mag_gain(self, gain):
		"""Set the magnetometer's gain.
		@param int gain: One of the magnetometer gain constants.
		"""
        self._mag_gain = gain
        self._write_u8(_MAGTYPE, _REG_MAG_CRB_REG_M, self._mag_gain)
        if self._mag_gain == MAGGAIN_1_3:
            _LSM303MAG_GAUSS_LSB_XY = 1100.0
            _LSM303MAG_GAUSS_LSB_Z  = 980.0
        elif self._mag_gain == MAGGAIN_1_9:
            _LSM303MAG_GAUSS_LSB_XY = 855.0
            _LSM303MAG_GAUSS_LSB_Z  = 760.0
        elif self._mag_gain == MAGGAIN_2_5:
            _LSM303MAG_GAUSS_LSB_XY = 670.0
            _LSM303MAG_GAUSS_LSB_Z  = 600.0
        elif self._mag_gain == MAGGAIN_4_0:
            _LSM303MAG_GAUSS_LSB_XY = 450.0
            _LSM303MAG_GAUSS_LSB_Z  = 400.0
        elif self._mag_gain == MAGGAIN_4_7:
            _LSM303MAG_GAUSS_LSB_XY = 400.0
            _LSM303MAG_GAUSS_LSB_Z  = 355.0
        elif self._mag_gain == MAGGAIN_5_6:
            _LSM303MAG_GAUSS_LSB_XY = 330.0
            _LSM303MAG_GAUSS_LSB_Z  = 295.0
        elif self._mag_gain == MAGGAIN_8_1:
            _LSM303MAG_GAUSS_LSB_XY = 230.0
            _LSM303MAG_GAUSS_LSB_Z  = 205.0

    def set_mag_rate(self, rate):
		"Set the magnetometer update rate.
		@param int rate - One of the magnetometer rate constants.
		"""
        reg_m = ((rate & 0x07) << 2) & 0xFF
        self.write_u8(_MAGTYPE, _REG_MAG_CRA_REG_M, reg_m)


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
