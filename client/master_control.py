__author__ = 'mrreload'
import Tkinter as tk
ch = __import__('chat_client')
import time, Queue, threading, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import ConfigParser

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
# from gi.repository import GdkX11, GstVideo
from gi.repository import GdkX11, GstVideo

# GObject.threads_init()
Gst.init(None)
Empty = Queue.Empty


def show_video():
	p = Player()
	p.run()


class Player(object):
	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		#If the module is executed as a script __name__ will be '__main__' and sys.argv[0] will be the full path of the module.
		if __name__ == '__main__':
			path = os.path.split(sys.argv[0])[0]
		#Else the module was imported and it has a __file__ attribute that will be the full path of the module.
		else:
			path = os.path.split(__file__)[0]
		self.config.read(os.path.join(os.path.dirname(path), 'client.conf'))
		if len(self.config.sections()) <= 0:
			print "Config file not present, copying default"
			self.config.read(os.path.join(path, 'client.conf'))
			with open(os.path.join(os.path.dirname(path), 'client.conf'), "w") as conf:
				self.config.write(conf)

		global v_host
		v_host = self.config.get("Connection", "host")
		global v_port
		v_port = int(self.config.get("Connection", "video_port"))
		self.msg_q = Queue.Queue(maxsize=0)
		self.window = tk.Tk()
		self.window.title("PiBot Control")
		self.window.geometry('1280x740')
		self.window.protocol("WM_DELETE_WINDOW", self.exithandler)
		self.videoframe = tk.Frame(self.window, width=1280, height=720)
		self.menubar = tk.Menu(self.window)
		self.window.config(menu=self.menubar)
		self.fileMenu = tk.Menu(self.menubar)
		self.fileMenu.add_command(label="Configuration...", command=self.showConfig)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.window.quit)
		self.menubar.add_cascade(label="File", menu=self.fileMenu)

		# Keyboard bindings
		self.setup_key_binds()
		self.telemetry = tk.Label(self.window, text="Hello, world!", font=("Arial", 12), bg='black', fg="white")

		self.telemetry.place(relwidth=1, height=20)
		self.videoframe.pack(side=tk.BOTTOM, anchor=tk.S, expand=tk.YES, fill=tk.BOTH)
		self.window_id = self.videoframe.winfo_id()

		# Setup Messaging Connection
		self.chat = ch.chat_client()
		self.chat.connecttoserver()
		self.chat.receivedata(self.msg_q, self.chat.s, self)
		self.msg_q.put("Waiting for messages!")
		self.update_tele2()

		# Create GStreamer pipeline
		self.pipeline = Gst.Pipeline()

		# Create bus to get events from GStreamer pipeline
		self.bus = self.pipeline.get_bus()


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
				self.videoframe.bind(key, lambda event, arg=command: self.keypress(event, arg))
		self.videoframe.bind("<Button-1>", self.callback)

	def callback(self, event):
		self.videoframe.focus_set()
		print "clicked at", event.x, event.y

	def keypress(self, event, command):
		self.telemetry.config(text=command)
		self.telemetry.update_idletasks()
		self.chat.sendcommand(command)

	def run(self):
		self.setup_video()
		# Start the Gstreamer pipeline
		self.pipeline.set_state(Gst.State.PLAYING)
		# Open the Tk window
		self.window.mainloop()

	def quit(self, window):
		self.pipeline.set_state(Gst.State.NULL)
		self.window.destroy()

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
		self.telemetry.config(text=servertext)
		self.telemetry.update_idletasks()

	def update_tele2(self):
		if not self.msg_q.empty():
			servertext = self.msg_q.get_nowait()
			self.telemetry.config(text=servertext)
			self.telemetry.update_idletasks()
		self.telemetry.after(100, self.update_tele2)


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
		tcpsrc.set_property("host", v_host)
		tcpsrc.set_property("port", v_port)

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