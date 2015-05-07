__author__ = 'mrreload'
import Tkinter as tk
ch = __import__('chat_client')
import time, Queue, threading, os, sys, math
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import ConfigParser
import geo

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
		self.lidar_dist = 0
		self.pointlist = []
		self.counter = 0
		self.recording = False



	def do_real_init(self):
		# Initialize the tkinter gui
		self.showWindow()
		# Keyboard bindings
		self.setup_key_binds()
		# Setup Messaging Connection
		self.chat = ch.chat_client(self.host, self.message_port)
		self.chat.connecttoserver()
		self.chat.receivedata(self)
		self.msg_q.put("Waiting for messages!")
		self.update_tele2()
		self.screen_thread()

		# Create GStreamer pipeline
		self.pipeline = Gst.Pipeline()

		# Create bus to get events from GStreamer pipeline
		self.bus = self.pipeline.get_bus()

	def showWindow(self):
		# Setup main client gui
		self.window = tk.Tk()
		self.window.title("PiBot Control")
		self.window.geometry('1280x590')
		self.window.protocol("WM_DELETE_WINDOW", self.exithandler)
		self.window.configure(background="black")
		# Configure grid for stretchiness
		self.window.columnconfigure(0, weight=1)
		self.window.columnconfigure(1, weight=1)
		self.window.columnconfigure(2, weight=1)
		self.window.columnconfigure(3, weight=12)
		self.window.rowconfigure(0, weight=6)
		self.window.rowconfigure(1, weight=32)
		self.window.rowconfigure(2, weight=1)
		# Add frames for display
		self.compassFrame = tk.Frame(self.window, background="black")
		self.compassFrame.grid(row=0,column=0, sticky="nsew", padx=1, pady=1)
		self.lidarFrame = tk.Frame(self.window, background="black")
		self.lidarFrame.grid(row=0,column=1, sticky="nsew", padx=1, pady=1)
		self.gpsFrame = tk.Frame(self.window, background="black")
		self.gpsFrame.grid(row=0,column=2, sticky="nsew", padx=1, pady=1)
		self.mapFrame = tk.Frame(self.window, bg="yellow")
		self.mapFrame.grid(row=1,column=0,columnspan=3, sticky="nsew", padx=1, pady=1)
		self.videoFrame = tk.Frame(self.window, bg="")
		self.videoFrame.grid(row=0,column=3,rowspan=2, sticky="nsew", padx=1, pady=1)
		self.statusFrame = tk.Frame(self.window, background="white")
		self.statusFrame.grid(row=2,column=0,columnspan=4, sticky="nsew", padx=1, pady=1)
		# Add menu to gui
		self.menubar = tk.Menu(self.window)
		self.window.config(menu=self.menubar)
		self.fileMenu = tk.Menu(self.menubar)
		self.fileMenu.add_command(label="Configuration...", command=self.showConfig)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.window.quit)
		self.menubar.add_cascade(label="File", menu=self.fileMenu)
		# Initialize variables to update labels directly
		self.compassValue = tk.StringVar()
		self.compassValue.set("Compass!")
		self.headingValue = tk.StringVar()
		self.headingValue.set("Heading!")
		self.lidarValue = tk.StringVar()
		self.lidarValue.set("Lidar inches!")
		self.pantiltValue = tk.StringVar()
		self.pantiltValue.set("pantilt!")
		self.gpsValue = tk.StringVar()
		self.gpsValue.set("GPS!")
		self.statusValue = tk.StringVar()
		self.statusValue.set("Command!")
		self.recordValue = tk.StringVar()
		self.recordValue.set(0)

		# Add a record button to the status bar
		self.recordButton = tk.Button(self.statusFrame, text="Record", fg="white", bg="Green", padx=5, command=self.do_record)
		self.recordButton.pack(side=tk.RIGHT)

		# Add labels to frames
		self.compassLabel = tk.Label(self.compassFrame, textvariable=self.compassValue)
		self.compassLabel.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
		self.headingLabel = tk.Label(self.compassFrame, textvariable=self.headingValue)
		self.headingLabel.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
		self.lidarLabel = tk.Label(self.lidarFrame, textvariable=self.lidarValue)
		self.lidarLabel.pack(expand=tk.YES, fill=tk.BOTH)
		self.pantiltLabel = tk.Label(self.lidarFrame, textvariable=self.pantiltValue)
		self.pantiltLabel.pack(expand=tk.NO, fill=tk.BOTH)
		self.gpsLabel = tk.Label(self.gpsFrame, textvariable=self.gpsValue)
		self.gpsLabel.pack(expand=tk.YES, fill=tk.BOTH)
		self.recLabel = tk.Label(self.statusFrame, textvariable=self.recordValue)
		self.recLabel.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH)
		self.statusLabel = tk.Label(self.statusFrame, textvariable=self.statusValue)
		self.statusLabel.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

		# Pack a canvas into the map frame for plotting points
		self.mapCanvas = tk.Canvas(self.mapFrame, bg="white", width=1, height=1)
		self.mapCanvas.pack(expand=tk.YES, fill=tk.BOTH)
		self.mapCanvas.bind("<Configure>", self.mapresize)
		#set focus to video frame
		self.window.focus_set()
		self.window_id = self.videoFrame.winfo_id()

	def mapresize(self, event):
		# Clear current map for resize
		self.mapCanvas.delete(tk.ALL)
		self.mapCanvas_width, self.mapCanvas_height = event.width, event.height
		# Draw x-axis
		self.mapCanvas.create_line(0, self.mapCanvas_height/2, self.mapCanvas_width, self.mapCanvas_height/2, dash=2, arrow=tk.BOTH)
		# Draw y-axis
		self.mapCanvas.create_line(self.mapCanvas_width/2, 0, self.mapCanvas_width/2, self.mapCanvas_height, dash=2, arrow=tk.BOTH)
		for point in self.pointlist:
			self.plotpoint(*point)

	def plotpoint(self, x_center, y_center):
		# Convert from grid coords to real canvas coords
		x_center = (self.mapCanvas_width/2) + x_center
		y_center = (self.mapCanvas_height/2) - y_center
		# Plot the point as a circle centered on the coords given
		self.mapCanvas.create_oval(x_center-1, y_center-1, x_center+1, y_center+1, fill="red")

	def getpoint(self, degrees, distance):
		# Convert heading degrees to radians
		theta = math.radians(90-degrees)
		# Use trig to calculate coords
		x = distance*(math.cos(theta))
		y = distance*(math.sin(theta))
		z = 0
		# print x, y
		return x, y

	def newpoint(self):
		if self.lidar_dist != 0:
			x, y = self.getpoint(self.compass_heading+self.pan_angle, self.lidar_dist)
			self.pointlist.append([x, y])
			self.plotpoint(x, y)

	def do_record(self):
		if self.recording:
			self.recordButton.configure(text="Record", bg="green")
			print "Cancelling Record!"
			self.videoFrame.after_cancel(self.count)
			self.counter = 0
			self.recording = False
		else:
			self.recordButton.configure(text="Stop", bg="red")
			print "Start Record!"
			self.recording = True
			self.record_counter_update()


	def record_counter_update(self):
		self.counter += 1
		self.recordValue.set(self.counter)
		self.count = self.videoFrame.after(1000, self.record_counter_update)

	def showConfig(self):
		self.values = {}
		self.configWindow = tk.Toplevel(self.window)
		self.configWindow.title("Client Configuration")
		self.configFrame = tk.Frame(self.configWindow)
		rowindex = 0
		for section in self.config.sections():
			self.sectionLabel = {}
			self.sectionLabel[section] = tk.Label(self.configFrame, text=section)
			self.sectionLabel[section].grid(row=rowindex,column=0)
			rowindex += 1
			self.values[section] = dict(self.config.items(section))
			for label, entry in self.values[section].iteritems():
				self.values[section][label] = tk.StringVar()
				self.values[section][label].set(entry)
				self.valueLabel = {}
				self.valueLabel[label] = tk.Label(self.configFrame, text=label)
				self.valueLabel[label].grid(row=rowindex,column=0)
				self.valueEntry = {}
				self.valueEntry[label] = tk.Entry(self.configFrame, textvariable=self.values[section][label])
				self.valueEntry[label].grid(row=rowindex,column=1)
				rowindex += 1
		self.configFrame.pack(padx=50, pady=50)
		self.saveButton = tk.Button(self.configWindow, text="Save", command=self.saveConfig)
		self.saveButton.pack(side="bottom")
		self.configWindow.focus_set()

	def saveConfig(self):
		if __name__ == '__main__':
			path = os.path.split(sys.argv[0])[0]
		else:
			path = os.path.split(__file__)[0]
		for section, value in self.values.iteritems():
			for label, entry in value.iteritems():
				self.config.set(section, label, self.values[section][label].get())
		with open(os.path.join(os.path.dirname(path), 'client.conf'), "w") as conf:
			self.config.write(conf)
		print "Saved!"

	def setup_key_binds(self):
		keybindings = dict(self.config.items("KeyBindings"))
		for command, key in keybindings.iteritems():
			if isinstance(key, str):
				print "Binding %s to %s" % (key, command)
				self.window.bind(key, lambda event, arg=command: self.keypress(event, arg))
		self.window.bind("<Button-1>", self.callback)

	def callback(self, event):
		self.window.focus_set()
		print "clicked at", event.x, event.y

	def keypress(self, event, command):
		self.statusValue.set("Command sent: "+command)
		self.chat.sendcommand(command)

	def run(self):
		self.setup_video()
		# Start the Gstreamer pipeline
		self.pipeline.set_state(Gst.State.PLAYING)
		# Open the Tk window
		self.window.mainloop()

	def quit(self, window):
		print "Closing out"
		try:
			while 1:
				print "Q:" + self.msg_q.get_nowait()
		except Empty:
			print "Queue empty"
			pass
		print "Closing Video Stream"
		self.pipeline.set_state(Gst.State.NULL)
		print "Destroying root window"
		self.window.destroy()
		print "Quitting"
		self.window.quit()

	def on_sync_message(self, bus, message, w_id):
		if message.get_structure() is None:
			return
		if message.get_structure().get_name() == 'prepare-window-handle':
			#print('prepare-window-handle')
			image_sink = message.src
			image_sink.set_property('force-aspect-ratio', True)
			image_sink.set_window_handle(w_id)
		else:
			print("No Match")
			print(message.get_structure().get_name())

	def on_eos(self, bus, msg):
		print('on_eos(): seeking to start of video')
		self.pipeline.seek_simple(
			Gst.Format.TIME,
			Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
			0
		)

	def on_error(self, bus, msg):
		print('on_error():', msg.parse_error())

	def update_tele(self, servertext):
		self.statusValue.set(servertext)

	def update_tele2(self):
		if not self.msg_q.empty():
			servertext = self.msg_q.get_nowait()
			# self.statusValue.set(servertext)
		# self.window.after(100, self.update_tele2)

	def exithandler(self):
		print "Closing out"
		try:
			while 1:
				print "Q:" + self.msg_q.get_nowait()
		except Empty:
			print "Queue empty"
			pass
		print "Closing Video Stream"
		self.pipeline.set_state(Gst.State.NULL)
		print "Destroying root window"
		self.window.destroy()
		print "Quitting"
		self.window.quit()

	def setup_video(self):
		self.bus.add_signal_watch()
		self.bus.connect('message::eos', self.on_eos)
		self.bus.connect('message::error', self.on_error)

		# This is needed to make the video output in our DrawingArea:
		self.bus.enable_sync_message_emission()
		self.bus.connect('sync-message::element', self.on_sync_message, self.window_id)

		# Create GStreamer elements
		tcpsrc = Gst.ElementFactory.make("tcpclientsrc", "source")
		self.pipeline.add(tcpsrc)
		tcpsrc.set_property("host", self.host)
		tcpsrc.set_property("port", self.video_port)

		gdpdepay = Gst.ElementFactory.make("gdpdepay", "gdpdepay")
		self.pipeline.add(gdpdepay)
		tcpsrc.link(gdpdepay)

		rtph264depay = Gst.ElementFactory.make("rtph264depay", "rtph264depay")
		self.pipeline.add(rtph264depay)
		gdpdepay.link(rtph264depay)

		h264parse = Gst.ElementFactory.make("h264parse", "h264parse")
		self.pipeline.add(h264parse)
		rtph264depay.link(h264parse)

		if os.name == "posix":
			vaapidecode = Gst.ElementFactory.make("vaapidecode", "vaapidecode")
			self.pipeline.add(vaapidecode)
			h264parse.link(vaapidecode)

			vaapisink = Gst.ElementFactory.make("vaapisink", "vaapisink")
			self.pipeline.add(vaapisink)
			vaapisink.set_property("sync", "false")
			vaapidecode.link(vaapisink)
		else:
			avdec_h264 = Gst.ElementFactory.make("avdec_h264", "avdec_h264")
			self.pipeline.add(avdec_h264)
			h264parse.link(avdec_h264)

			videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
			self.pipeline.add(videoconvert)
			avdec_h264.link(videoconvert)

			autovideosink = Gst.ElementFactory.make("autovideosink", "autovideosink")
			self.pipeline.add(autovideosink)
			autovideosink.set_property("sync", "false")
			videoconvert.link(autovideosink)

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
							self.lidarValue.set(str(self.lidar_dist)+" in")
							self.newpoint()
						if sn[1] == "Compass":
							self.compassValue.set(geo.direction_name(float(sn[2])))
							self.compass_heading = float("{0:.2f}".format(float(sn[2])))
							self.headingValue.set(self.compass_heading)
						if sn[1] == "GPS":
							self.gpsValue.set(sn[2])
						if sn[1] == "PanTilt":
							self.pantiltValue.set("pan: "+sn[2]+" tilt: "+sn[3])
							self.pan_angle = float(sn[2])
							self.tilt_angle = float(sn[3])
			time.sleep(.5)

if __name__ == "__main__":
	p = Player()
	p.do_real_init()
	p.run()




