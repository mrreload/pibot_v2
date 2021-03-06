__author__ = 'marc.hoaglin'
import zmq
import threading
import sys, time
from random import randint, random


def tprint(msg):
	"""like print, but won't get newlines confused with multiple threads"""
	sys.stdout.write(msg + '\n')
	sys.stdout.flush()


class ServerTask(threading.Thread):
	"""ServerTask"""

	def __init__(self):
		threading.Thread.__init__(self)
		config = {}
		execfile("server.conf", config)
		self.m_port = str(config["msg_port"])

	def run(self):
		print 'server starting on: ' + self.m_port
		context = zmq.Context()
		frontend = context.socket(zmq.ROUTER)
		frontend.bind('tcp://*:' + self.m_port)

		backend = context.socket(zmq.DEALER)
		backend.bind('inproc://sensors')
		#
		# workers = []
		# for i in range(5):
		# 	worker = ServerWorker(context)
		# 	worker.start()
		# 	workers.append(worker)

		poll = zmq.Poller()
		poll.register(frontend, zmq.POLLIN)
		poll.register(backend, zmq.POLLIN)

		while True:
			sockets = dict(poll.poll())
			if frontend in sockets:
				ident, msg = frontend.recv_multipart()
				tprint('Server received %s id %s' % (msg, ident))
				backend.send_multipart([ident, msg])
			if backend in sockets:
				ident, msg = backend.recv_multipart()
				tprint('Sending to frontend %s id %s' % (msg, ident))
				frontend.send_multipart([ident, msg])

		frontend.close()
		backend.close()
		context.term()


class ServerWorker(threading.Thread):
	"""ServerWorker"""

	def __init__(self, context):
		threading.Thread.__init__(self)
		self.context = context

	def run(self):
		worker = self.context.socket(zmq.DEALER)
		worker.connect('inproc://sensors')
		tprint('Worker started')
		while True:
			ident, msg = worker.recv_multipart()
			tprint('Worker received %s from %s' % (msg, ident))
			replies = randint(0, 4)
			for i in range(replies):
				time.sleep(1. / (randint(1, 10)))
				worker.send_multipart([ident, msg])

		worker.close()


class ClientTask(threading.Thread):
	"""ClientTask"""

	def __init__(self, id):
		self.id = id
		threading.Thread.__init__(self)

	def run(self):
		context = zmq.Context()
		socket = context.socket(zmq.DEALER)
		identity = u'worker-%d' % self.id
		socket.identity = identity.encode('ascii')
		socket.connect('tcp://localhost:8001')
		print('Client %s started' % (identity))
		poll = zmq.Poller()
		poll.register(socket, zmq.POLLIN)
		reqs = 0
		data = "DATATYPE"
		while True:
			reqs = reqs + 1
			print('Req #%d sent..' % (reqs))
			socket.send_string(u'request #%d' % (reqs))
			for i in range(5):
				sockets = dict(poll.poll(1000))
				if socket in sockets:
					msg = socket.recv()
					tprint('Client %s received: %s' % (identity, msg))

		socket.close()
		context.term()


def main():
	"""main function"""
	server = ServerTask()
	server.start()
	for i in range(3):
		client = ClientTask(i)
		client.start()
	server.join()


if __name__ == "__main__":
	main()