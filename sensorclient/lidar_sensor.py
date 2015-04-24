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
sensor_address =
def lidar_init():
	fd =