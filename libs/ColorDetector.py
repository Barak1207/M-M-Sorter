#import sys
#import PIL
#import cv2
from cv2 import VideoCapture, imwrite
from time import sleep, time
#import webcolors

class ColorDetector():
	DEFAULT_TOLERANCE = 40
	def __init__(self, camera_index=0):
		self.cam = VideoCapture(camera_index)

	def capture_image(self, retry=5):
		for i in xrange(retry):
			self.cam.read()
		s, img = self.cam.read()
		if s:
			return img
		else:
			raise('Can\'t take pic!')
			return False

	def distance_colors(self, color_a, color_b):
		#Tuple of RGB
		#Might be physically incorrect, but for this purpose it might suffice, returns value of 0-255
		#Might have to address intensity of colors---
		return (abs(color_a[0] - color_b[0]) + abs(color_a[1] - color_b[1]) + abs(color_a[2] - color_b[2]))/3

	def is_new_color(self, existing_colors, new_color, tolerance=DEFAULT_TOLERANCE):
		#Takes a list of existing_colors(tuples of RGB) and checks if new_colors is different by TOLERANCE from the existing_colors
		#Returns a tuple of (is_new, resembles_what)		
		for existing_color in existing_colors:
			distance = self.distance_colors(existing_color, new_color)
			if distance < tolerance:#There's a color which resembles the new color
				return (False, existing_color)#Return; this is not a new color and return the color which resembles it
		return (True, None)

	def find_similar_color(self, existing_colors, new_color, starting_tolerance=DEFAULT_TOLERANCE, tolerance_step=15):
		#Find a similar color at all cost!!
		is_new_color = True
		tolerance = starting_tolerance
		while is_new_color:
			is_new_color, similar_color = self.is_new_color(existing_colors, new_color, tolerance=tolerance)
			tolerance += tolerance_step
		return similar_color

	def average_color(self, image):
		height, width, channels = image.shape
		assert channels == 3

		height_calc = width_calc = min(height, width)/2
		count_calc = height_calc*width_calc#Calc a square from the original image

		height_offset = (height_calc - height_calc)/2
		width_offset = (width_calc - width_calc)/2

		sum_R = 0
		sum_G = 0
		sum_B = 0
		for i in xrange(height_calc):
			for j in xrange(width_calc):
				pixel = image[i + height_offset][j + width_offset]
				#Notice that cv2 Image is BGR format and not RGB!
				sum_B += pixel[0]#B
				sum_G += pixel[1]#G
				sum_R += pixel[2]#R
		return (sum_R/count_calc, sum_G/count_calc, sum_B/count_calc)#return RGB not BGR tuple

	def close(self):
		self.cam.release()
	#Using CV2 images



if __name__ == "__main__":

	try:
		cam = ColorDetector()
		while True:
			raw_input('Press to capture an image...')
			img = cam.capture_image()
			print ('Snap!')
			raw_input('Press to average color')
			avg_color = cam.average_color(img)
			print 'Average color: ' + str(avg_color)			
	except KeyboardInterrupt:
		pass
	except Exception, e:
		print e
	finally:
		cam.close()
