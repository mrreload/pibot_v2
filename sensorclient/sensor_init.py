__author__ = 'mrreload'
import shlex, sys, subprocess
from time import sleep
schat = __import__('sensor_chat')
sensor = __import__('lidar_sensor')

class SensorMain(object):
	def __init__(self):
		config = {}
		execfile("sensor.conf", config)
		args = config["sensor_command"]
		self.cmd = shlex.split(args)
		self.saddr = config["i2c_address"]
		self.sc = schat.sensor_chat()
		self.sc.connecttoserver()


	def run_cmd(self):
		result = "hello"
		try:
			result = subprocess.check_output(self.cmd)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		return result

	def get_sensor_data(self):
		sens = sensor.Lidar_Lite(self.saddr)
		return sens.read_sensor()

	def snd_msg(self, msg):
		self.sc.sendcommand(msg)


p = SensorMain()
# output = p.run_cmd()
# p.snd_msg(output)
# print("output: " + output)

while True:
	sleep(1)
	p.snd_msg(p.get_sensor_data())




