from time import time, sleep
import RPi.GPIO as GPIO
import traceback
from cv2 import VideoCapture#, imwrite

import ColorDetector
import StepperMotor
import LinearSelenoid

AVAILABLE_ANGLES = [0.0, 10.0, 20.0, 30.0, 40.0]
STANDBY_LED = 19
PAUSE_RESUME_BUTTON = 13
SELENOID_PIN = 	26
STEPPER_MOTOR_IN1 = 4
STEPPER_MOTOR_IN2 = 17
STEPPER_MOTOR_IN3 = 23
STEPPER_MOTOR_IN4 = 24

keep_going = True


def init_gpio():
	GPIO.setmode(GPIO.BCM)
#	GPIO.setup(SELENOID_PIN, GPIO.OUT)
#	GPIO.setup(STEPPER_MOTOR_IN1, GPIO.OUT)
#	GPIO.setup(STEPPER_MOTOR_IN2, GPIO.OUT)
#	GPIO.setup(STEPPER_MOTOR_IN3, GPIO.OUT)
#	GPIO.setup(STEPPER_MOTOR_IN4, GPIO.OUT)
	GPIO.setup(STANDBY_LED, GPIO.OUT)
	GPIO.setup(PAUSE_RESUME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#	GPIO.output(SELENOID_PIN, False)
#	GPIO.output(STEPPER_MOTOR_IN1, False)
#	GPIO.output(STEPPER_MOTOR_IN2, False)
#	GPIO.output(STEPPER_MOTOR_IN3, False)
#	GPIO.output(STEPPER_MOTOR_IN4, False)
	GPIO.output(STANDBY_LED, False)

def exit_gpio():
#	GPIO.output(SELENOID_PIN, False)
#	GPIO.output(STEPPER_MOTOR_IN1, False)
#	GPIO.output(STEPPER_MOTOR_IN2, False)
#	GPIO.output(STEPPER_MOTOR_IN3, False)
#	GPIO.output(STEPPER_MOTOR_IN4, False)
	GPIO.output(STANDBY_LED, False)
	GPIO.cleanup()

def pause_resume(channel):
	global keep_going
	keep_going = not keep_going


class AngleGenerator():
	def __init__(self, angle_list):
		self.angles = angle_list
		self.len_angles = len(self.angles)
		self.angle_index = 0
	def new_angle_available(self):
		return self.angle_index <= self.len_angles - 1
	def new_angle(self):
	#	if self.new_angle_available():
		to_return = None
		try:
			to_return = self.angles[self.angle_index]
			self.angle_index += 1
		except:
			raise "No angles available"
		finally:
			return to_return
		#else:
		#	return False
	def reset(self):
		self.angle_index = 0

#def next_available_angle():
#	for angle in AVAILABLE_ANGLES:
#		yield angle

if __name__ == "__main__":
	try:
		init_gpio()

		color_detector = ColorDetector.ColorDetector()
		stepper_motor = StepperMotor.StepperMotor(STEPPER_MOTOR_IN1, STEPPER_MOTOR_IN2, STEPPER_MOTOR_IN3, STEPPER_MOTOR_IN4)
		linear_selenoid = LinearSelenoid.LinearSelenoid(SELENOID_PIN)
		angle_generator = AngleGenerator(AVAILABLE_ANGLES)

		color_to_angle = {}
		#angle_generator = next_available_angle()
		new_angle = 0.0		

		print 'Waiting...'
		GPIO.output(STANDBY_LED, True)
		#GPIO.wait_for_edge(PAUSE_RESUME_BUTTON, GPIO.RISING)#Wait for first button press

		GPIO.add_event_detect(PAUSE_RESUME_BUTTON, GPIO.RISING, callback=pause_resume, bouncetime=1000)

		while keep_going:
			
			image = color_detector.capture_image()
			print 'Snap!'
			new_color = color_detector.average_color(image)#Color of candy currently right above the linear selenoid
			print 'Current average color: ' + str(new_color)

#			if angle_generator.new_angle_available():
#				is_new_color, similar_color = color_detector.is_new_color(color_to_angle.keys(), new_color)
#				if is_new_color:
#					new_angle = angle_generator.new_angle()
#					color_to_angle[new_color] = new_angle					
#					print 'New color detected: ' + str(new_color)
#				else:
#					new_angle = color_to_angle[similar_color]
#					print 'Similar color detected, original: ' + str(new_color) + ', similar: ' + str(similar_color)
#			else:#No angles remaining
#				similar_color = color_detector.find_similar_color(color_to_angle.keys(), new_color)
#				new_angle = color_to_angle[similar_color]
#				print 'No containers(angles) left, original: ' + str(new_color) + ', similar(est): ' + str(similar_color)
			print 'Current angle is: ' + str(stepper_motor.get_current_angle())
			new_angle = float(raw_input('Enter new angle: '))
			print 'Moving motor ' + str(stepper_motor.get_current_angle()) + '->' + str(new_angle)
			stepper_motor.step_to_angle(new_angle)
			raw_input('Press Enter to release...')
			linear_selenoid.retract_and_extend(delay=0.5)

			#sleep(3)

	except Exception, e:
		traceback.print_exc()
	finally:
		print 'Exiting, cleaning up...'
		exit_gpio()
		color_detector.close()
		stepper_motor.close()
		linear_selenoid.close()
