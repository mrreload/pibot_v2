__author__ = 'mrreload'
import shlex, sys, subprocess, threading
import time
schat = __import__('sensor_chat')
sensor1 = __import__('lidar_sensor')
sensor2 = __import__('compass')


class SensorMain(object):
	def __init__(self):
		config = {}
		execfile("/home/pi/pibot_v2/sensorclient/sensor.conf", config)
		args = config["sensor_command"]
		self.cmd = shlex.split(args)
		self.saddr = config["i2c_address"]
		self.sc = schat.sensor_chat()
		self.sc.connecttoserver()
		self.sens1 = sensor1.Lidar_Lite(self.saddr)
		self.sens2 = sensor2.Compass()

	def run_cmd(self):
		result = "hello"
		try:
			result = subprocess.check_output(self.cmd)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		return result

	def lidar(self):
		while True:
			self.snd_msg("Lidar," + str(self.sens1.read_sensor()) + "," + str(self.sens1.read_status()) + "," + str(round(time.time(), 2)))
			time.sleep(1)

	def compass(self):
		while True:
			self.snd_msg("Compass," + str(self.sens2.get_bearing())+ "," + str(round(time.time(), 2)))
			time.sleep(.5)

	def snd_msg(self, msg):
		self.sc.send_data("Sensor," + msg + ";")

	def spawn_threads(self):
		t1 = threading.Thread(name="lidar", target=self.lidar)
		t1.setDaemon(True)
		t1.start()

		t2 = threading.Thread(name="compass", target=self.compass)
		t2.setDaemon(True)
		t2.start()
		while True:
			time.sleep(2)


p = SensorMain()
# output = p.run_cmd()
# p.snd_msg(output)
# print("output: " + output)

p.spawn_threads()




