# Save as server.py
# Message Receiver
import os
from Queue import Queue
from Adafruit_PWM_Servo_Driver import PWM
from ServoHATDriver import stdServo

pc = __import__('picontrol')


class MessageServ(object):
	def __init__(self):
		pwm = PWM(0X40)
		# stdServo(pwm, frequency, channel, servoRange, minPulse, maxPulse, debug=False)
		self.pan = stdServo(pwm, 50, 1, 180, 500, 2710)
		self.tilt = stdServo(pwm, 50, 0, 180, 500, 2710)
		self.degree_to_move = 5
		# set to center
		self.pan.moveToDegree(0)
		self.tilt.moveToDegree(0)
		self.q = Queue()

	def read_command(self, data):
		data = data.strip()

		print "Received message: " + data
		if data == "exit":
			os.exit(1)
		# motor controls
		elif data == "left":
			pc.go_left()
		elif data == "right":
			pc.go_right()
		elif data == "forward":
			pc.go_forward()
		elif data == "backward":
			pc.go_backward()
		elif data == "stop":
			pc.do_stop()
		# pan tilt controls
		elif data == "sweep_left":
			self.pan.moveToMin()
		elif data == "sweep_right":
			self.pan.moveToMax()
		elif data == "sweep_up":
			self.tilt.moveToMin()
		elif data == "sweep_down":
			self.tilt.moveToMax()
		elif data == "tilt_up":
			self.tilt.addDegree(-self.degree_to_move)
		elif data == "tilt_down":
			self.tilt.addDegree(self.degree_to_move)
		elif data == "pan_left":
			self.pan.addDegree(-self.degree_to_move)
		elif data == "pan_right":
			self.pan.addDegree(self.degree_to_move)
		elif data == "reset":
			self.pan.moveToDegree(0)
			self.tilt.moveToDegree(0)
		elif data == "sweep":
			print("Not implemented!")  #os._exit(0)
		else:
			print("What happened?", data)

		# Return the current position oof the pan and tilt servos in degrees
		return self.pan.curDegree, self.tilt.curDegree