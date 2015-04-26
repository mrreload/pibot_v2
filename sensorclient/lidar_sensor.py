#!/usr/bin/python
__author__ = 'marc.hoaglin'

from Adafruit_I2C import Adafruit_I2C
from time import sleep
i2c_address = 0x62

class Lidar_Lite(Adafruit_I2C):
	# Lidar Lite address
	sensor_address = Adafruit_I2C(0x62)
	MEASURE_REG = 0x00
	MEASURE_VAL = 0x04
	DISTANCE_REG_HI = 0x0f
	DISTANCE_REG_LO = 0x10

	STATUS_REG = 0x47
	VERSION_REG = 0x41

	# ERROR_READ -1

	# Status Bits
	STAT_BUSY = 0x01
	STAT_REF_OVER = 0x02
	STAT_SIG_OVER = 0x04
	STAT_PIN = 0x08
	STAT_SECOND_PEAK = 0x10
	STAT_TIME = 0x20
	STAT_INVALID = 0x40
	STAT_EYE = 0x80

	def read_sensor(self):

		hival = Adafruit_I2C.write8(self.sensor_address, self.MEASURE_REG, self.MEASURE_VAL)
		sleep(.01)

		loval = Adafruit_I2C.readU8(self.sensor_address, self.DISTANCE_REG_LO)

		hival = Adafruit_I2C.readS8(self.sensor_address, self.DISTANCE_REG_HI)
		return ((hival << 8) + loval)






