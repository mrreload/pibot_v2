__author__ = 'mrreload'

ch = __import__('chat_client')
import time, Queue, threading, os, sys, math
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import ConfigParser
import geo

from collections import OrderedDict

import clientgui

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
# from gi.repository import GdkX11, GstVideo
from gi.repository import GdkX11, GstVideo

# GObject.threads_init()
Gst.init(None)
Empty = Queue.Empty

class Player(object):
	def __init__(self):
		# Grab and parse the client.conf file
		self.config = ConfigParser.ConfigParser()
		# If the module is executed as a script __name__ will be '__main__' and sys.argv[0] will be the full path of the module.
		if __name__ == '__main__':
			path = os.path.split(sys.argv[0])[0]
		# Else the module was imported and it has a __file__ attribute that will be the full path of the module.
		else:
			path = os.path.split(__file__)[0]
		self.config.read(os.path.join(os.path.dirname(path), 'client.conf'))
		if len(self.config.sections()) <= 0:
			print "Config file not present, copying default"
			self.config.read(os.path.join(path, 'client.conf'))
			with open(os.path.join(os.path.dirname(path), 'client.conf'), "w") as conf:
				self.config.write(conf)
		# Set variables for host and port
		self.host = self.config.get("Connection", "host")
		self.video_port = int(self.config.get("Connection", "video_port"))
		self.message_port = int(self.config.get("Connection", "message_port"))
		# Set the message queue
		self.msg_q = Queue.Queue(maxsize=0)
		# Something for gps?
		my_lon = 33.6880290
		my_lat = 117.9861210
		hb = geo.xyz(my_lat, my_lon)
		la = geo.xyz(34.0522340, -118.2436850)
		true_north = geo.great_circle_angle(hb, la, geo.geographic_northpole)
		print "True North " + str(true_north)
		self.compass_heading = 0
		self.pan_angle = 0
		self.tilt_angle = 0
		self.lidar_dist = 0
		self.pointlist = []
		self.lidarDict = OrderedDict()
		self.compassDict = OrderedDict()
		self.panDict = OrderedDict()
		self.tiltDict = OrderedDict()

		# Setup Messaging Connection
		self.chat = ch.chat_client(self.host, self.message_port)
		self.chat.connecttoserver()
		self.chat.receivedata(self)
		self.msg_q.put("Waiting for messages!")
		self.update_tele2()
		self.screen_thread()

		# Initialize the tkinter gui
		self.gui = clientgui.gui(self)

	def update_tele(self, servertext):
		self.gui.statusValue.set(servertext)

	def update_tele2(self):
		if not self.msg_q.empty():
			servertext = self.msg_q.get_nowait()
			# self.statusValue.set(servertext)
		# self.window.after(100, self.update_tele2)

	def screen_thread(self):
		worker2 = threading.Thread(name="msgblitter", target=self.blitmsg, args=(self.msg_q,))
		worker2.setDaemon(True)
		worker2.start()

	def blitmsg(self, mq):
		while True:
			# print "Outer Loop"
			while not mq.empty():
				# print "getting data from Q"
				time.sleep(.1)
				dmsg = mq.get()
				# print("Queue data: " + dmsg)
				tm_arry = dmsg.split(';')
				for cmd in tm_arry:
					sn = cmd.split(',')
					if sn[0] == "Sensor":
						if sn[1] == "Lidar":
							self.lidar_dist = float(sn[2])*0.39370
							self.gui.lidarValue.set(str(self.lidar_dist)+" in")
							self.gui.map.newpoint()
						if sn[1] == "Compass":
							self.gui.compassValue.set(geo.direction_name(float(sn[2])))
							self.compass_heading = float("{0:.2f}".format(float(sn[2])))
							self.gui.headingValue.set(self.compass_heading)
						if sn[1] == "GPS":
							self.gui.gpsValue.set(sn[2])
						if sn[1] == "PanTilt":
							self.gui.pantiltValue.set("pan: "+sn[2]+" tilt: "+sn[3])
							self.pan_angle = float(sn[2])
							self.tilt_angle = -1*(float(sn[3]))
							# print self.pan_angle, self.tilt_angle
							self.panDict.update({sn[4]: sn[2]})
							self.tiltDict.update({sn[4]: sn[3]})
			time.sleep(.5)

if __name__ == "__main__":
	p = Player()
	p.gui.run()




