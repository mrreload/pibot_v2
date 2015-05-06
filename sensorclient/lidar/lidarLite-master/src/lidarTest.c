    #include "../include/lidarLite.h"
    #include <time.h>

    int main(int argc,char *argv[])
    {
    int fd, res, i, del;
    unsigned char st, ver;
    const double cm_to_inch = 2.54; // (0.39);

// First arg is delay in ms (default is 1000)
if (argc > 1) 
   del = atoi(argv[1]);
else del=1000;

	float cm, inches;
        int feet;    
    fd = lidar_init(true);
    printf("Calibrating");
    LidarLiteCalibrate();
    printf("Calibrated %x with %x", CALI_REG, CALI_OFFSET)
    if (fd == -1) {
        printf("initialization error\n");
        }
    else {        
            res = lidar_read(fd);
            st = lidar_status(fd);
            //ver = lidar_version(fd);
	    cm = (float)res;
            inches = (float)res / cm_to_inch;

            feet = inches/12;

            //inches = inches-(feet*12);
	    //printf("%.1f cm = %d feet, %.1f inches\n", cm, feet, inches);
            printf("%3.0d \n", res);
	    
            //lidar_status_print(st);
            
            //delay(del);
           
        }
    }
