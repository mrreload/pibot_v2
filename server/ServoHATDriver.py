import time

def printStat(description, value, debug):
	if debug:
		if value.is_integer():
			print "%s: %d" % (description, value)
		else:
			print "%s: %f" % (description, value)

class stdServo(object):
	def __init__(self, pwm, frequency, channel, servoRange, minPulse, maxPulse, debug=False):
		self.frequency = float(frequency)		#Set frequency in Hertz
		self.channel = int(channel)			#channel of this servo
		self.servoRange = float(servoRange)	#The range of the servo in degrees
		self.minPulse = float(minPulse)		#The pulse required for 0 degrees in us(microseconds)
		self.maxPulse = float(maxPulse)		#The pulse required for max degrees in us
		self.timePerTick = (1000000/self.frequency)/4096				#Time per tick in us
		self.timePerDegree = (self.maxPulse-self.minPulse)/self.servoRange	#Also in us
		self.pwm = pwm
		self.pwm.setPWMFreq(frequency)		#set the frequency to send in Hertz
		self.debug = debug
		self.curDegree = 0
		self.maxDegree = self.servoRange/2
		self.minDegree = self.maxDegree*-1
		self.curPulse = (self.maxPulse-self.minPulse)/2
		self.setPulse(self.curPulse)
		printStat("Channel", self.channel, self.debug)
		printStat("Time per tick", self.timePerTick, self.debug)
		printStat("Time per degree", self.timePerDegree, self.debug)

	def moveToDegree(self, desiredDegree):
		desiredDegree = int(desiredDegree)
		printStat("Input degree", desiredDegree, self.debug)
		if desiredDegree > self.maxDegree:
			desiredDegree = self.maxDegree
		elif desiredDegree < self.minDegree:
			desiredDegree = self.minDegree
		realDegree = desiredDegree+self.maxDegree
		printStat("Translated degree", realDegree, self.debug)
		desiredPulse = (realDegree*self.timePerDegree)+self.minPulse		#Also in us
		printStat("Desired pulse", desiredPulse, self.debug)
		endTick = int((desiredPulse)/self.timePerTick)	#Final calculation
		printStat("Pulse ending tick", endTick, self.debug)
		self.curDegree = desiredDegree
		self.curPulse = desiredPulse
		self.pwm.setPWM(self.channel, 0, endTick)		#Sends the signal
		return True

	def setPulse(self, desiredPulse):
		printStat("Input pulse", desiredPulse, self.debug)
		if desiredPulse > self.maxPulse:
			desiredPulse = self.maxPulse
		elif desiredPulse < self.minPulse:
			desiredPulse = self.minPulse
		endTick = int(desiredPulse/self.timePerTick)	#convert to ticks
		desiredDegree = (((endTick*self.timePerTick)-self.minPulse)/self.timePerTick)-self.maxDegree
		printStat("Desired degree", desiredDegree, self.debug)
		printStat("Pulse ending tick", endTick, self.debug)
		self.curDegree = desiredDegree
		self.curPulse = desiredPulse
		self.pwm.setPWM(self.channel, 0, endTick)			#Sends the signal
		return True

	def backAndForth(self, degreeBuffer, degreePerIteration, timePerSweep):
		minDegree = self.minDegree+degreeBuffer
		maxDegree = self.maxDegree-degreeBuffer
		timePerSweep = float(timePerSweep)
		sleepTime = (timePerSweep/(maxDegree*2))/1000	#time between each step in loop in ms
		printStat("Time per step(sec)", sleepTime, self.debug)
		minDegree = int(minDegree)
		maxDegree = int(maxDegree)
		for degree in range(minDegree, maxDegree):
			self.moveToDegree(degree)
			time.sleep(sleepTime)
		for degree in range(maxDegree, minDegree, -1):
			self.moveToDegree(degree)
			time.sleep(sleepTime)
		return True

	def manualPulse(self):
		pulse = int(raw_input("Desired pulse in us:"))
		while(pulse!=0):
			self.setPulse(pulse)
			pulse = int(raw_input("Desired pulse in us:"))
		return True

	def stop(self):
		self.pwm.setPWM(self.channel, 0, 4096)
		return True

	def addDegree(self, degree):
		self.moveToDegree(self.curDegree+degree)

	def moveToMin(self):
		self.moveToDegree(self.minDegree)

	def moveToMax(self):
		self.moveToDegree(self.maxDegree)

	def calibrate(self):
		minpulse = self.minPulse
		maxpulse = self.maxPulse
		print "Previous values: %d Min %d Max" % (self.minPulse, self.maxPulse)
		self.minPulse = 0
		self.maxPulse = 5000
		if debug:
			print "Pulse Restrictions off."
		pulse = int(raw_input("Enter guess for Minimum pulse:"))
		while(pulse!=0):
			minpulse = pulse
			self.setPulse(minpulse)
			print "Enter 0 to confirm, or"
			pulse = int(raw_input("Enter another guess for Minimum pulse:"))
		pulse = int(raw_input("Enter guess for Maximum pulse:"))
		while(pulse!=0):
			maxpulse = pulse
			self.setPulse(maxpulse)
			print "Enter 0 to confirm, or"
			pulse = int(raw_input("Enter another guess for Maximum pulse:"))
		print "Entered values: %d Min %d Max" % (minpulse, maxpulse)
		confirm = raw_input("Save these values? (y/n):")
		while True:
			if(confirm="y"):
				self.minPulse = minpulse
				self.maxPulse = maxpulse
				print "Values saved and set."
				break
			elif(confirm="n"):
				print "Values trashed."
				break
			else:
				confirm = raw_input("Please enter \"y\" or \"n\":")

class contServo(object):
	def __init__(self, pwm, frequency, channel, neutralPulse, minPulse, maxPulse, revTime, Trim, debug=False):
		self.frequency = float(frequency)		#Set frequency in Hertz
		self.channel = int(channel)			#channel of this servo
		self.neutralPulse = float(neutralPulse)	#The range of the servo in degrees
		self.minPulse = float(minPulse)		#The pulse required for 0 degrees in us(microseconds)
		self.maxPulse = float(maxPulse)		#The pulse required for max degrees in us
		self.revTime = float(revTime)		#time in seconds for servo to move 360 degrees at 100% speed
		self.Trim = float(Trim)
		self.neutralTick = int(round((self.neutralPulse*4096)/(1000000/self.frequency))) #convert neutral to ticks
		self.minTick = int(round((self.minPulse*4096)/(1000000/self.frequency))) #convert minimum
		self.maxTick = int(round((self.maxPulse*4096)/(1000000/self.frequency))) #convert maximum
		self.pwm = pwm
		self.pwm.setPWMFreq(frequency)		#set the frequency to send in Hertz
		self.debug = debug

	def setSpeed(self, direction, speed):
		#sanitize speed
		speed = int(speed)
		if speed > 100:
			speed = 100
		elif speed < 0:
			speed = 0
		#check direction and calculate pulse
		if direction == 'cw':
			pulse = int(round(self.neutralTick-((speed*(self.neutralTick-self.minTick))/100)))
		else:
			pulse = int(round(self.neutralTick+((speed*(self.maxTick-self.neutralTick))/100)))
		#send the signal
		#print 'Set channel %d to pulse %d.' % (channel, pulse)
		self.pwm.setPWM(self.channel, 0, pulse)

	def servoSweep(self, speed):
		sweepTime = round(((100/speed)*self.revTime)/4, 2)
		print 'Sweep Time %f seconds' % sweepTime
		self.setSpeed('cw', speed)
		time.sleep(sweepTime*(1-self.Trim))
		self.setSpeed('ccw', speed)
		time.sleep(sweepTime*(1+self.Trim))

	def servoRotateLeft(self, angle, speed):
		angle = int(angle)
		#sanitize speed
		speed = int(speed)
		if speed > 100:
			speed = 100
		elif speed < 0:
			speed = 0
		sweepTime = round(((100/speed)*self.revTime)/(360/angle), 2)
		print "Setting laser to the left of target."
		print "Sweep Time %f seconds at %d%%" % (sweepTime, speed)
		self.setSpeed('ccw', speed)
		time.sleep(sweepTime)
		self.stop()

	def runSweep(self, sweeps, minspeed):
		print 'Executing Channel %d with %d number of sweeps.' % (channel, sweeps)
		sweeps = int(sweeps)
		if(sweeps > 50):
			sweeps = 50
		if(sweeps <= 1):
			print 'Last sweep, %d%% speed' % minspeed
			self.servoSweep(minspeed)
		elif(sweeps == 2):
			print 'Sweep 1, 100%% speed'
			self.servoSweep(100)
			print 'Last sweep, %d%% speed' % minspeed
			self.servoSweep(minspeed)
		else:
			print 'Sweep 1, 100%% speed'
			self.servoSweep(100)
			increment = int((100-minspeed)/(sweeps-1))
			speed = increment
			for sweep in range(2, sweeps):
				if(speed < minspeed):
					speed = minspeed
				elif(speed > 100):
					speed = 100
				print 'Sweep %d, %d%% speed' % (sweep, speed)
				self.servoSweep(speed)
				speed += increment
			print 'Last sweep, %d%% speed' % minspeed
			self.servoSweep(minspeed)
		print 'Sweeping complete, resetting Channel %d.' % channel
		self.stop()


	def stop():
		self.pwm.setPWM(self.channel, 0, 4096)

	def manual():
		print 'Starting Servo Check...'
		direction = raw_input('Direction (cw or ccw): ')
		speed = int(raw_input('Speed (1-100): '))
		while(speed != 0):
			print 'Setting Channel %d to %d%% speed...' % (self.channel, speed)
			self.setSpeed(direction, speed)
			print 'Enter 0 to quit.'
			speed = int(raw_input('Speed (1-100): '))
		self.stop()

	def center():
		self.setSpeed(self.channel, 'cw', 10)
		raw_input('Press ENTER when centered.')
		self.stop()

	def scan():
		print 'Starting Scan...'
		self.center()
		self.servoRotateLeft(45, 10)
		print 'Ready for scanning.'
		sweeps = int(raw_input('How many sweeps per scan? (0-50): '))
		scans = int(raw_input('How many scans per angle?: '))
		rotations = int(raw_input('How many angles to scan?: '))
		if(rotations >= 1):
			moveangle = int(360/rotations)
			for rotation in range(0, rotations):
				for scan in range(0, scans):
					self.runSweep(sweeps, 10)
				print 'Scan Complete.'
				if(rotation+1 < rotations):
					moveangle += int(360/rotations)
		self.stop()
		print 'LaserScan is finished.'