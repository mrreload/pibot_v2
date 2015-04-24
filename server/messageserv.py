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
		elif data == "L":
			pc.go_left()
		elif data == "R":
			pc.go_right()
		elif data == "F":
			pc.go_forward()
		elif data == "B":
			pc.go_backward()
		elif data == "LS":
			pc.stop_left()
		elif data == "RS":
			pc.stop_right()
		elif data == "FS":
			pc.stop_forward()
		elif data == "BS":
			pc.stop_backward()
		elif data == "S":
			pc.do_stop()
		elif data == "Sweep_Left":
			self.pan_move = self.pan_min
			pt.pan(self.pan_move)
		elif data == "Sweep_Right":
			self.pan_move = self.pan_max
			pt.pan(self.pan_move)
		elif data == "Sweep_Up":
			self.tilt_move = self.tilt_min
			pt.tilt(self.tilt_move)
		elif data == "Sweep_Down":
			self.tilt_move = self.tilt_max
			pt.tilt(self.tilt_move)
		elif data == "Tilt_Up":
			print("so far so good.")
			self.tilt_move -= 5
			if self.tilt_move >= self.tilt_min:
				pt.tilt(self.tilt_move)
			else:
				print("Min Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move += 5
		elif data == "Tilt_Down":
			self.tilt_move += 5
			if self.tilt_move <= self.tilt_max:
				pt.tilt(self.tilt_move)
			else:
				print("Max Tilt Already reached, ignoring move request " + str(self.tilt_move))
				self.tilt_move -= 5
		elif data == "Pan_Left":
			self.pan_move -= 5
			if self.pan_move >= self.pan_min:
				pt.pan(self.pan_move)
			else:
				print("Min Pan Already reached, ignoring move request " + str(self.pan_move))
				self.pan_move += 5
			# pt.pan(pan_move)
		elif data == "Pan_Right":
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

