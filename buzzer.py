import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)

def beep(repeat):
   for i in range(0, repeat):
      for pulse in range(60): # square wave loop
         GPIO.output(15, True)
         time.sleep(0.005)     # high for .001 sec
         GPIO.output(15, False)      
         time.sleep(0.005)     # low for .001 sec
      time.sleep(0.02)        # add a pause between each cycle


beep(1)

