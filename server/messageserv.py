# Save as server.py 
# Message Receiver
import os

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

	def read_data(self, data):
		data = data.strip()

		print "Received message: " + data
		if data == "exit":
			os.exit(1)
		elif data == "Left":
			pc.go_left()
		elif data == "Right":
			pc.go_right()
		elif data == "Forward":
			pc.go_forward()
		elif data == "Backward":
			pc.go_backward()
		# elif data == "LS":
		# 	pc.stop_left()
		# elif data == "RS":
		# 	pc.stop_right()
		# elif data == "FS":
		# 	pc.stop_forward()
		# elif data == "BS":
		# 	pc.stop_backward()
		elif data == "Stop":
			pc.do_stop()
		elif data == "SweepLeft":
			self.pan_move = self.pan_min
			pt.pan(self.pan_move)
		elif data == "SweepRight":
			self.pan_move = self.pan_max
			pt.pan(self.pan_move)
		elif data == "SweepUp":
			self.tilt_move = self.tilt_min
			pt.tilt(self.tilt_move)
		elif data == "SweepDown":
			self.tilt_move = self.tilt_max
			pt.tilt(self.tilt_move)
		elif data == "TiltUp":
			self.tilt_move -= 5
			if self.tilt_move >= self.tilt_min:
				pt.tilt(self.tilt_move)
			else:
				print("Min Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move += 5
		elif data == "TiltDown":
			self.tilt_move += 5
			if self.tilt_move <= self.tilt_max:
				pt.tilt(self.tilt_move)
			else:
				print("Max Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move -= 5
		elif data == "PanLeft":
			self.pan_move -= 5
			if self.pan_move >= self.pan_min:
				pt.pan(self.pan_move)
			else:
				print("Min Pan Already reached, ignoring move request " + str(self.pan_move))
				self.pan_move += 5
			# pt.pan(pan_move)
		elif data == "PanRight":
			self.pan_move += 5
			if self.pan_move <= self.pan_max:
				pt.pan(self.pan_move)
			else:
				print("Max Pan already reached, ignoring move request " + str(self.pan_move))
				self.pan_move -= 5
			# pt.pan(pan_move)
		elif data == "Reset":
			pt.reset()
			self.pan_move = self.pan_def
			self.tilt_move = self.tilt_def
		elif data == "Sweep":
			print("Not implemented!")  #os._exit(0)
		else:
			print("What happened?")

