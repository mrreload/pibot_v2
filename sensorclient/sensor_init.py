__author__ = 'mrreload'
import shlex, sys, subprocess
schat = __import__('sensor_chat')

class SensorMain(object):
	def __init__(self):
		config = {}
		execfile("sensor.conf", config)
		args = config["sensor_command"]
		self.cmd = shlex.split(args)
		self.sc = schat.sensor_chat()
		self.sc.connecttoserver()

	def run_cmd(self):
		result = "hello"
		try:
			result = subprocess.check_output(self.cmd)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		return result

	def snd_msg(self, msg):
		self.sc.sendcommand(msg)


p = SensorMain()
output = p.run_cmd()
p.snd_msg(output)
print("output: " + output)




