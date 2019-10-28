This library is archived and no longer supported
=============================================
This library has been split into separate libararies for the magnetometer and accelerometer. The accelerometer code will  be shared with another version of the LSM303 that uses the same accelerometer but not the magnetometer and this repo will be archived.

This library will no longer be supported. Please us the new libraries

The new, split libraries

https://github.com/adafruit/Adafruit_CircuitPython_LSM303_Accel

https://github.com/adafruit/Adafruit_CircuitPython_LSM303DLH_Mag

The library for the new magnetometer

https://github.com/adafruit/Adafruit_CircuitPython_LSM303AGR_Mag

You can find usage information for the new libraries in the sensor's guide:

https://learn.adafruit.com/lsm303-accelerometer-slash-compass-breakout/python-circuitpython

Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-lsm303/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/lsm303/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_LSM303.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_LSM303
    :alt: Build Status

Adafruit CircuitPython module for the LSM303 6-DoF with 3-axis accelerometer and magnetometer

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-lsm303/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-lsm303

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-lsm303

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-lsm303
    
Usage Example
=============

.. code-block:: python

	import time
	import board
	import busio

	import adafruit_lsm303

	i2c = busio.I2C(board.SCL, board.SDA)
	sensor = adafruit_lsm303.LSM303(i2c)

	while True:
		raw_accel_x, raw_accel_y, raw_accel_z = sensor.raw_acceleration
		accel_x, accel_y, accel_z = sensor.acceleration
		raw_mag_x, raw_mag_y, raw_mag_z = sensor.raw_magnetic
		mag_x, mag_y, mag_z = sensor.magnetic

		print('Acceleration raw: ({0:6d}, {1:6d}, {2:6d}), (m/s^2): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_accel_x, raw_accel_y, raw_accel_z, accel_x, accel_y, accel_z))
		print('Magnetometer raw: ({0:6d}, {1:6d}, {2:6d}), (gauss): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_mag_x, raw_mag_y, raw_mag_z, mag_x, mag_y, mag_z))
		print('')
		time.sleep(1.0)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_LSM303/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
