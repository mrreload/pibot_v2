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

class Lidar_Lite(Adafruit_I2C):
	# Lidar Lite address

	MEASURE_VAL = 0x04

	STATUS_REG  = 0x47
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





if __name__ == '__main__':

	from time import sleep
	sensor_address = Adafruit_I2C(0x62)
	print Adafruit_I2C.getPiRevision()
	print Adafruit_I2C.getPiI2CBusNumber()
	# lid = Lidar_Lite()
	MEASURE_REG = 0x00
	MEASURE_VAL = 0x04
	DISTANCE_REG_HI = 0x0f
	DISTANCE_REG_LO = 0x10
	while True:
		print "write hi"
		hiVal = Adafruit_I2C.write8(sensor_address, MEASURE_REG, MEASURE_VAL)
		sleep(.02)
		print "read lo"
		loVal = Adafruit_I2C.readU8(sensor_address, DISTANCE_REG_LO)
		print "read hi"
		hiVal = Adafruit_I2C.readS8(sensor_address, DISTANCE_REG_HI)
		print hiVal
		print loVal
		print ((hiVal << 8) + loVal)
		sleep(1)