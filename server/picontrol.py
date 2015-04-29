#!/usr/bin/python
__author__ = 'mrreload'
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import curses, sys, traceback
import os
import pygame

#os.environ['SDL_VIDEODRIVER'] = 'dummy'
#pygame.init()
#screen = pygame.display.set_mode((100,100))
#clock = pygame.time.Clock()
#window = curses.initscr()
#window.nodelay(0)
#window.keypad(1)
ch = -1
stop = 1
f_speed = 225
b_speed = 175
turn_speed = 175
oturn_speed = 150
mh = Adafruit_MotorHAT(addr=0x60)
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
myMotor3 = mh.getMotor(3)
myMotor4 = mh.getMotor(4)
myMotor1.run(Adafruit_MotorHAT.RELEASE)
myMotor2.run(Adafruit_MotorHAT.RELEASE)
myMotor3.run(Adafruit_MotorHAT.RELEASE)
myMotor4.run(Adafruit_MotorHAT.RELEASE)


def do_stop():
    print("STOP")
    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    myMotor3.run(Adafruit_MotorHAT.RELEASE)
    myMotor4.run(Adafruit_MotorHAT.RELEASE)

def go_forward():
    print "Forward! "
    myMotor1.run(Adafruit_MotorHAT.FORWARD)
    myMotor2.run(Adafruit_MotorHAT.FORWARD)
    myMotor3.run(Adafruit_MotorHAT.FORWARD)
    myMotor4.run(Adafruit_MotorHAT.FORWARD)
    myMotor1.setSpeed(f_speed)
    myMotor2.setSpeed(f_speed)
    myMotor3.setSpeed(f_speed)
    myMotor4.setSpeed(f_speed)
    #myMotor1.run(Adafruit_MotorHAT.RELEASE)

def go_backward():
    print "Backward! "
    myMotor1.run(Adafruit_MotorHAT.BACKWARD)
    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
    myMotor3.run(Adafruit_MotorHAT.BACKWARD)
    myMotor4.run(Adafruit_MotorHAT.BACKWARD)    
    myMotor1.setSpeed(b_speed)
    myMotor2.setSpeed(b_speed)
    myMotor3.setSpeed(b_speed)
    myMotor4.setSpeed(b_speed)
    #myMotor1.run(Adafruit_MotorHAT.RELEASE)

def go_left():
    myMotor1.run(Adafruit_MotorHAT.BACKWARD)
    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
    myMotor3.run(Adafruit_MotorHAT.FORWARD)
    myMotor4.run(Adafruit_MotorHAT.FORWARD)
    myMotor3.setSpeed(turn_speed)
    myMotor4.setSpeed(turn_speed)
    myMotor1.setSpeed(oturn_speed)
    myMotor2.setSpeed(oturn_speed)    

def go_right():
    myMotor1.run(Adafruit_MotorHAT.FORWARD)
    myMotor2.run(Adafruit_MotorHAT.FORWARD)
    myMotor3.run(Adafruit_MotorHAT.BACKWARD)
    myMotor4.run(Adafruit_MotorHAT.BACKWARD)
    myMotor1.setSpeed(turn_speed)
    myMotor2.setSpeed(turn_speed)
    myMotor3.setSpeed(oturn_speed)
    myMotor4.setSpeed(oturn_speed)

def stop_forward():
    print "Stop Forward! "
    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    myMotor3.run(Adafruit_MotorHAT.RELEASE)
    myMotor4.run(Adafruit_MotorHAT.RELEASE)    

def stop_backward():
    print "Stop Backward! "
    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    myMotor3.run(Adafruit_MotorHAT.RELEASE)
    myMotor4.run(Adafruit_MotorHAT.RELEASE)

def stop_left():
    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    myMotor3.run(Adafruit_MotorHAT.RELEASE)
    myMotor4.run(Adafruit_MotorHAT.RELEASE)   

def stop_right():
    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    myMotor3.run(Adafruit_MotorHAT.RELEASE)
    myMotor4.run(Adafruit_MotorHAT.RELEASE)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


atexit.register(turnOffMotors)

# def main():
#     while stop == 1:
#     	pygame.event.pump()
#     	for event in pygame.event.get():
#         	if event.type == pygame.QUIT:
#             		crashed = True
#
#         ############################
#         	if event.type == pygame.KEYDOWN:
#             		if event.key == pygame.K_LEFT:
#                 		print "Left!"
# 				go_left()
# 	    		elif event.key == pygame.K_RIGHT:
#                 		print "Right!"
# 				go_right()
# 	    		elif event.key == pygame.K_UP:
# 				print "Forward!"
# 				go_forward()
# 	    		elif event.key == pygame.K_DOWN:
# 				print "Back!"
# 				go_backward()
# 	    		elif event.key == pygame.K_SPACE:
# 				print "Stop!"
# 				do_stop()
# 	    		elif event.key == pygame.K_ESCAPE:
# 				print "Exit!"
# 				pygame.quit()
# 				quit()
#         	elif event.type == pygame.KEYUP:
#             		if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
#                 		print "Key released!"
        ######################
    ##
    
   ##         
    
    #clock.tick(60)
    # put code continuously run here
   # ch = window.getch()
   # print ("getkey: " + str(ch) + "\n")
   # if ch == curses.KEY_UP:
    #    print("FORWARD!\n")
#	go_forward()
    #if ch == curses.KEY_DOWN:
     #   print("BACK!\n")
#	go_backward()
#    if ch == curses.KEY_LEFT:
#        print("LEFT!\n")
#	go_left()
#    if ch == curses.KEY_RIGHT:
#        print("RIGHT!\n")
#	go_right()
#    if ch == 32:
#        print("STOP!\n")
#	do_stop()
#    if ch == 48:
#        stop == ch
#        print("Exiting.. " + str(ch))
#        curses.nocbreak()
#        window.keypad(0)
#        curses.echo()
#        curses.endwin()
#        sys.exit(99)
        # else :
        # print(ch)


#print(str(ch))
    #pygame.exit()
    #exit()

