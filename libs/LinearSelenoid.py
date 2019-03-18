import RPi.GPIO as GPIO
from time import sleep






class LinearSelenoid():
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(self.pin, False)
	def retract(self):
		GPIO.output(self.pin, True)
	def extend(self):
		GPIO.output(self.pin, False)
	def retract_and_extend(self, delay):
		GPIO.output(self.pin, True)
		sleep(delay)
		GPIO.output(self.pin, False)
	def close(self):
		GPIO.output(self.pin, False)



if __name__ == "__main__":

	try:
		SELENOID_PIN = 	26
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(SELENOID_PIN, GPIO.OUT)
		GPIO.output(SELENOID_PIN, False)

		sele = LinearSelenoid(SELENOID_PIN)
		
		while True:
			#raw_input('Press to retract and extend')
			#sele.retract_and_extend(0.1)
			raw_input('Press to retract')
			sele.retract()
			raw_input('Press to extend')
			sele.extend()
	except KeyboardInterrupt:
		pass
	except Exception, e:
		print e
	finally:
		GPIO.output(SELENOID_PIN, False)
		GPIO.cleanup()
