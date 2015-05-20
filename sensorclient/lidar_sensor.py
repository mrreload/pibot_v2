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

	ERROR_READ = -1

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
		sleep(.02)
		loval = self.read_raw(self.DISTANCE_REG_LO, False)
		hival = self.read_raw(self.DISTANCE_REG_HI, True)
		return ((hival << 8) + loval)

	def read_status(self):
		value = "okay"
		status = Adafruit_I2C.readU8(self.sensor_address, self.STATUS_REG)
		if (status & self.STAT_BUSY):
			value = "busy"
		if (status & self.STAT_REF_OVER):
			value = "reference overflow"
		if (status & self.STAT_SIG_OVER):
			value = "signal overflow"
		if (status & self.STAT_PIN):
			value = "mode select pin"
		if (status & self.STAT_SECOND_PEAK):
			value = "second peak"
		if (status & self.STAT_TIME):
			value = "active between pairs"
		if (status & self.STAT_INVALID):
			value = "no signal"
		if (status & self.STAT_EYE):
			value = " eye safety"
		return value

	def read_raw(self, reg, allowZero):
		i = 0
		value = ""
		sleep(.001)
		while True:
			value = Adafruit_I2C.readU8(self.sensor_address, reg)
			if value == self.ERROR_READ or (value == 0 and not allowZero):
				sleep(.02)
				if i > 50:
					print "Timeout"
					return self.ERROR_READ
				i += 1
			else:
				return val