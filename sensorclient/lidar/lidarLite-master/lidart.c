    #include "include/lidarLite.h"
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
    
    fd = lidar_init(false);
   
    if (fd == -1) {
        printf("initialization error\n");
        }
    else {
        for (i=0;i<40;i++) {
            res = lidar_read(fd);
            st = lidar_status(fd);
            //ver = lidar_version(fd);
            inches = cm / cm_to_inch;;

            feet = inches/12;

            inches = inches-(feet*12);
	    printf("%.1f cm = %d feet, %.1f inches\n", cm, feet, inches);
            printf("%3.0d cm \n", res);
	    
            lidar_status_print(st);
            
            delay(del);
            }
        }
    }
