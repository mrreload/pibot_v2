import os
from Queue import Queue
from Adafruit_PWM_Servo_Driver import PWM
from ServoHATDriver import stdServo


pwm = PWM(0X40)
# stdServo(pwm, frequency, channel, servoRange, minPulse, maxPulse, debug=False)
self.pan = stdServo(pwm, 50, 0, 180, 500, 2710)
self.tilt = stdServo(pwm, 50, 3, 190, 500, 2710)

self.pan.calibrate()