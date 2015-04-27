__author__ = 'mrreload'

import socket, select, string, sys, threading, time
import Queue



class sensor_chat(object):
	def __init__(self):
		config = {}
		execfile("sensor.conf", config)
		self.m_host = config["host"]
		self.m_port = config["message_port"]
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.settimeout(2)
		# self.msg_q = Queue.Queue(maxsize=0)

	def listenmsg(self, mq, sl, th):
		blconnected = True
		while blconnected:
			socket_list = [sl]

			# Get the list sockets which are readable
			read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

			for sock in read_sockets:
				#incoming message from remote server
				if sock == sl:
					data = sock.recv(4096)
					if not data:
						print '\nDisconnected from chat server'
						blconnected = False
					else:
						#print data
						sys.stdout.write(data)
						# th.msg_q.put(data)
						# th.update_tele(data)

					# self.prompt()
				time.sleep(.1)
		self.connecttoserver()
		blconnected = True


	def connecttoserver(self):
		try:
			self.s.connect((self.m_host, self.m_port))
		except:
			print("Unable to connect to: " + self.m_host + ":" + str(self.m_port))
			sys.exit()

		print 'Connected to remote host. Start sending messages'


	def send_data(self, cmnd):
		print("Sending Message: " + cmnd)
		self.s.sendall(cmnd)

	def receivedata(self, msgq, sockm, pthr):
		pthr.msg_q.put("Startup init")
		worker1 = threading.Thread(name="msgworker", target=self.listenmsg, args=(msgq, sockm, pthr))
		worker1.setDaemon(True)
		worker1.start()
		# master = mc.Player()
		time.sleep(.5)






