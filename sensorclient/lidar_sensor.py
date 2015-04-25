#!/usr/bin/python
__author__ = 'marc.hoaglin'
# int lidar_read(int fd) {
#            int hiVal, loVal, i=0;
#
#            // send "measure" command
#            hiVal = wiringPiI2CWriteReg8(fd, MEASURE_REG, MEASURE_VAL);
#            if (_dbg) printf("write res=%d\n", hiVal);
#            delay(20);
#
#            // Read second byte and append with first
#            loVal = _read_byteNZ(fd, DISTANCE_REG_LO) ;
#            if (_dbg) printf(" Lo=%d\n", loVal);
#
#            // read first byte
#            hiVal = _read_byte(fd, DISTANCE_REG_HI) ;
#            if (_dbg) printf ("Hi=%d ", hiVal);
#
#            return ( (hiVal << 8) + loVal);
#     }
# int lidar_init(bool dbg) {
#             int fd;
#             _dbg = dbg;
#             if (_dbg) printf("LidarLite V0.1\n\n");
#             fd = wiringPiI2CSetup(LIDAR_LITE_ADRS);
#             if (fd != -1) {
#                 lidar_status(fd);  // Dummy request to wake up device
#                 delay (100);
#                 }
#             return(fd);
#             }
# unsigned char lidar_status(int fd) {
#             return( (unsigned char) wiringPiI2CReadReg8(fd, STATUS_REG) );
#             }
from Adafruit_I2C import Adafruit_I2C
from time import sleep


class Lidar_Lite(Adafruit_I2C):
	# Lidar Lite address
	sensor_address = Adafruit_I2C(0x62)
	MEASURE_REG = 0x00
	MEASURE_VAL = 0x04
	DISTANCE_REG_HI = 0x0f
	DISTANCE_REG_LO = 0x10


	STATUS_REG = 0x47
	DISTANCE_REG_HI = 0x0f
	DISTANCE_REG_LO = 0x10
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
		print "write hi"
		hival = Adafruit_I2C.write8(self.sensor_address, self.MEASURE_REG, self.MEASURE_VAL)
		sleep(.02)
		print "read lo"
		loval = Adafruit_I2C.readU8(self.sensor_address, self.DISTANCE_REG_LO)
		print "read hi"
		hival = Adafruit_I2C.readS8(self.sensor_address, self.DISTANCE_REG_HI)
		print ((hival << 8) + loval)
		sleep(1)

l = Lidar_Lite()
l.read_sensor()




