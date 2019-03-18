import RPi.GPIO as GPIO
from time import sleep

class StepperMotor:
	#Honestly, I'm not quite sure what's the difference between a half and a full step, I'll check later,
	#Anyways, we need to do 4096 half\full steps for a rotation in my specific model.
	#Why it's 4096 for both full and half step? I don't know.
	#With a stride of 5.625 and a gear ratio of 64, we need (360/5.625)*64 = 4096 steps (as in, calls to __set_step__), I think.

	#Speed varation ratio: 1/64
	#Stride Angle: 5.625 / 64
	GEAR_RATIO = 64
	STRIDE_ANGLE = 5.625 / GEAR_RATIO
	ROTATION_STEPS = int(360.0 / STRIDE_ANGLE)
	SEQUENCE = [[1,0,0,0],#This is different from most guides!!~Barak
				[1,1,0,0],
				[0,1,0,0],
				[0,1,1,0],
				[0,0,1,0],
				[0,0,1,1],
				[0,0,0,1],
				[1,0,0,1]]
	SEQUENCE_REVERSE = SEQUENCE[::-1]
	
	HALF_STEP_DELAY = 0.0007
	FULL_STEP_DELAY = 0.002

	ANGLE_FILE = 'stpmtrang.dat'

	def __init__(self, IN1, IN2, IN3, IN4):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(IN1, GPIO.OUT)
		GPIO.output(IN1, False)
		GPIO.setup(IN2, GPIO.OUT)
		GPIO.output(IN2, False)
		GPIO.setup(IN3, GPIO.OUT)
		GPIO.output(IN3, False)
		GPIO.setup(IN4, GPIO.OUT)
		GPIO.output(IN4, False)

		self.pins = [IN1, IN2, IN3, IN4]
		self.angle_file = open(StepperMotor.ANGLE_FILE, 'a+')
		self.__update_angle__(self.__read_angle__())
		#self.step_to_angle(0.0)#Why is this here?

	def __write_angle__(self, angle):
		self.angle_file.seek(0)
		self.angle_file.truncate()
		self.angle_file.write(str(angle))
		self.angle_file.seek(0)
	def __read_angle__(self):
		try:
			self.angle_file.seek(0)
			angle = self.angle_file.read(3)
			self.angle_file.seek(0)
			if angle:
				return float(angle) % 360.0
			else:#File didn't exist, and we read an empty string
				return 0.0
		except IOError:
			return 0.0
	def __update_angle__(self, angle):
		self.current_angle = float(angle)
		self.__write_angle__(self.current_angle)
	def steps_to_angle(self, steps):
		return (360.0 * (steps / StepperMotor.ROTATION_STEPS))
	def angle_to_steps(self, angle):
		return int(StepperMotor.ROTATION_STEPS * abs((angle / 360.0)))

	def __set_step__(self, seq_step):
		#seq_step is a line from SEQUENCE
		for pin, step_pin_value in zip(self.pins, seq_step):
			GPIO.output(pin, step_pin_value)
	def __do_steps__(self, num_steps, seq, delay):
		s_len = len(seq)
		for i in xrange(num_steps):
			self.__set_step__(seq[i%s_len])
			sleep(delay)

	def steps(self, num_steps, reverse=False, is_full_step=False):
		seq = StepperMotor.SEQUENCE_REVERSE if reverse else StepperMotor.SEQUENCE
		seq = seq[::2] if is_full_step else seq
		delay = StepperMotor.is_full_step_DELAY if is_full_step else StepperMotor.HALF_STEP_DELAY
		self.__do_steps__(num_steps, seq, delay)
		
		self.__update_angle__(self.steps_to_angle(num_steps))

	def step_to_angle(self, angle_b, is_full_step=False):#From current angle
		delta = (angle_b - self.current_angle)# % 360.0 Modulo doesn't work well for negative numbers!
		if delta != 0.0:
			num_steps = self.angle_to_steps(delta)#int(abs((delta / 360.0 ) * StepperMotor.ROTATION_STEPS))
			self.steps(num_steps, reverse=delta<0 , is_full_step=is_full_step)

			self.__update_angle__(angle_b)
	def get_current_angle(self):
		return self.current_angle

	def close(self):
		for pin in self.pins:
			GPIO.output(pin, False)
		self.angle_file.close()





if __name__ == "__main__":
	GPIO.setmode(GPIO.BCM)
	pins = [4,17,23,24]#Connect like this https://tutorials-raspberrypi.de/wp-content/uploads/2014/08/uln2003-Steckplatine.png
	stp_motor = StepperMotor(*pins)
	

	try:
		while True:
			print 'Current angle is ' + str(stp_motor.get_current_angle())
			select = raw_input("'a' to change angle, 's' to make steps: ")
			if select.lower() is 'a':
				new_angle = float(raw_input("Change angle to: "))
				stp_motor.steps_to_angle(new_angle)
			elif select.lower() is 's':
				num_steps = int(raw_input("How many steps forward? (negative for backwards)"))
				stp_motor.steps(num_steps, reverse=num_steps<0)


	# End program cleanly with keyboard
	except KeyboardInterrupt:
		pass
	except Exception, e:
		print e
	finally:
		stp_motor.close()
		GPIO.cleanup()
