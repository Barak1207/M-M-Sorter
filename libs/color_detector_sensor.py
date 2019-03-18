import RPi.GPIO as GPIO
import time



s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10
NUM_VALIDATION = 3
DELAY = 0.1

class RGB:
  def __init__(R, G, B):
    self.R = R
    self.G = G
    self.B = B
  def main_color(self):
    return sorted([self.R, self.G, self.B], reverse=True)[0]    



def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")


def detect_RGB():
  for i in xrange(NUM_VALIDATION):

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(DELAY)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(DELAY)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(DELAY)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    
  

  colors = sorted([red, green, blue], reverse=True)
  if colors[0] == red:
    print 'Red'
  elif colors[0] == green:
    print 'Green'
  elif colors[0] == blue:
    print 'Blue'
  else:
    print 'IDK'


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        endprogram()
