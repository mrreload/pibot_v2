# Save as server.py 
# Message Receiver
import os
from Queue import Queue

pt = __import__('pantilt')
pc = __import__('picontrol')


class MessageServ(object):
	def __init__(self):
		self.pan_def = pt.pan_center
		self.tilt_def = pt.tilt_center
		self.pan_min = 0
		self.pan_max = 180
		self.tilt_min = 0
		self.tilt_max = 100
		self.pan_move = self.pan_def
		#global tilt_move
		self.tilt_move = 50
		pt.pan(self.pan_def)
		pt.tilt(self.tilt_def)
		self.q = Queue()

	def read_command(self, data):
		data = data.strip()

		print "Received message: " + data
		if data == "exit":
			os.exit(1)
		elif data == "left":
			pc.go_left()
		elif data == "right":
			pc.go_right()
		elif data == "forward":
			pc.go_forward()
		elif data == "backward":
			pc.go_backward()
		# elif data == "LS":
		# 	pc.stop_left()
		# elif data == "RS":
		# 	pc.stop_right()
		# elif data == "FS":
		# 	pc.stop_forward()
		# elif data == "BS":
		# 	pc.stop_backward()
		elif data == "stop":
			pc.do_stop()
		elif data == "sweep_left":
			self.pan_move = self.pan_min
			pt.pan(self.pan_move)
		elif data == "sweep_right":
			self.pan_move = self.pan_max
			pt.pan(self.pan_move)
		elif data == "sweep_up":
			self.tilt_move = self.tilt_min
			pt.tilt(self.tilt_move)
		elif data == "sweep_down":
			self.tilt_move = self.tilt_max
			pt.tilt(self.tilt_move)
		elif data == "tilt_up":
			self.tilt_move -= 5
			if self.tilt_move >= self.tilt_min:
				pt.tilt(self.tilt_move)
			else:
				print("Min Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move += 5
		elif data == "tilt_down":
			self.tilt_move += 5
			if self.tilt_move <= self.tilt_max:
				pt.tilt(self.tilt_move)
			else:
				print("Max Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move -= 5
		elif data == "pan_left":
			self.pan_move -= 5
			if self.pan_move >= self.pan_min:
				pt.pan(self.pan_move)
			else:
				print("Min Pan Already reached, ignoring move request " + str(self.pan_move))
				self.pan_move += 5
			# pt.pan(pan_move)
		elif data == "pan_right":
			self.pan_move += 5
			if self.pan_move <= self.pan_max:
				pt.pan(self.pan_move)
			else:
				print("Max Pan already reached, ignoring move request " + str(self.pan_move))
				self.pan_move -= 5
			# pt.pan(pan_move)
		elif data == "reset":
			pt.reset()
			self.pan_move = self.pan_def
			self.tilt_move = self.tilt_def
		elif data == "sweep":
			print("Not implemented!")  #os._exit(0)
		else:
			print("What happened?", data)
		print "Reached the end of doom"

