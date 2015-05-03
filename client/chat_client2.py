__author__ = 'mrreload'
import zmq
import os, sys
import ConfigParser

class ClientTask():
	"""ClientTask"""

	def __init__(self):
		self.config = ConfigParser.ConfigParser()
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

		self.m_host = self.config.get("Connection", "host")
		self.m_port = self.config.get("Connection", "message_port")
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.DEALER)
		self.identity = 'my-client'
		self.poll = zmq.Poller()

	def receive_msg(self):
		# socket.connect('tcp://localhost:5570')
		print('Client %s started' % (self.identity))
		reqs = 0

		while True:
			reqs = reqs + 1
			self.socket.send_string(u'request #%d' % (reqs))
			for i in range(5):
				sockets = dict(self.poll.poll(1000))
				if self.socket in sockets:
					msg = self.socket.recv()
					print('Client %s received: %s' % (self.identity, msg))

		self.socket.close()
		self.context.term()

	def server_connect(self):
		self.socket.connect('tcp://' + self.m_host + ':' + self.m_port)
		print('Client %s started' % (self.identity))

		self.poll.register(self.socket, zmq.POLLIN)

		self.socket.identity = self.identity.encode('ascii')


c = ClientTask()
c.server_connect()
c.receive_msg()
