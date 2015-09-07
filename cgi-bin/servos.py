#!/usr/bin/python

import sys
import argparse
from Adafruit_PWM_Servo_Driver import PWM
import time
import RPi.GPIO as GPIO
#import pigpio

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=False)
#GPIO = pigpio.pi()


# low end: 281 (1ms)
#high end: 562 (2ms)

servoMin = 281  # Min pulse length out of 4096
servoMax = 562  # Max pulse length out of 4096

PWM_OPEN = 370 #500
PWM_CLOSE = 300

PWM_LEFT = 330
PWM_RIGHT = 360

PWM_SEL_1 = 298
PWM_SEL_2 = 340
PWM_SEL_3 = 390
PWM_SEL_4 = 455

def readEncoder():
  num = 0
  num = num + (GPIO.input(40))
  num = num + (GPIO.input(31)*2)
  num = num + (GPIO.input(32)*4)
  num = num + (GPIO.input(33)*8)
  num = num + (GPIO.input(35)*16)
  num = num + (GPIO.input(36)*32)
  num = num + (GPIO.input(37)*64)
  num  = num + (GPIO.input(38)*128)
  #sys.stderr.write("Encoder Position: %d" % num)
  return num

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  #print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  #print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def setup():
  pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(40 ,GPIO.IN)
  GPIO.setup(31 ,GPIO.IN)
  GPIO.setup(32 ,GPIO.IN)
  GPIO.setup(33 ,GPIO.IN)
  GPIO.setup(35 ,GPIO.IN)
  GPIO.setup(36 ,GPIO.IN)
  GPIO.setup(37 ,GPIO.IN)
  GPIO.setup(38 ,GPIO.IN)

def select(position):
  if(position == 0):
    pwm.setPWM(5, 0, PWM_SEL_1)
  elif(position == 1):
    pwm.setPWM(5, 0, PWM_SEL_2)
  elif(position == 2):
    pwm.setPWM(5, 0, PWM_SEL_3)
  elif(position == 3):
    pwm.setPWM(5, 0, PWM_SEL_4)

def turn(direction):
  if(direction == 0): #stop
    pwm.setPWM(0, 0, 0)
  elif(direction == 1): #right
    pwm.setPWM(0, 0, PWM_RIGHT)
  elif(direction == -1): #left
    pwm.setPWM(0, 0, PWM_LEFT)

def rotateTo(position):
  sys.stderr.write("rotating to %d \n" % position)
  if(position < 15):
    decoder=[1,219,2,223,8,127,16,254,64,253,12,247,48,175,192,187]
    pos = decoder[position]
    enc = readEncoder()
    while enc != pos:
      turn(1)
      enc = readEncoder()
    turn(0)

def open(channel):
  sys.stderr.write('open channel: %d\n' % channel)
  if(channel == 0):
    pwm.setPWM(1, 0, PWM_OPEN-30)
  elif(channel == 1):
    pwm.setPWM(2, 0, PWM_OPEN-65)
  elif(channel == 2):
    pwm.setPWM(3, 0, PWM_OPEN+10)
  elif(channel == 3):
    pwm.setPWM(4, 0, PWM_OPEN-90)

def close(channel):
  sys.stderr.write('close channel: %d\n' % channel)
  if(channel == 0):
    pwm.setPWM(1, 0, PWM_CLOSE-30)
  elif(channel == 1):
    pwm.setPWM(2, 0, PWM_CLOSE-65)
  elif(channel == 2):
    pwm.setPWM(3, 0, PWM_CLOSE+10)
  elif(channel == 3):
    pwm.setPWM(4, 0, PWM_CLOSE-90)

def encoderLight(on):
  pwm.setPWM(8,0,4095*on);

def load(x,y):
  sys.stderr.write('loading ')
  sys.stderr.write('x: %d ' % x)
  sys.stderr.write('y: %d\n' % y)
  setup()
  rotateTo(y)
  select(x)
  turn(0)

def dispense(x,y):
  sys.stderr.write('dispensing ')
  sys.stderr.write('x: %d ' % x)
  sys.stderr.write('y: %d\n' % y)
  setup()
  rotateTo((y+8)%16)
  open(x)
  time.sleep(1)
  close(x)
  turn(0)

def goHome():
  setup()
  close(0)
  time.sleep(1)
  close(1)
  time.sleep(1)
  close(2)
  time.sleep(1)
  close(3)
  time.sleep(1)
  rotateTo((8)%16) # output 0
  time.sleep(1)
  pwm.setPWM(1, 0, 0)
  time.sleep(1)
  pwm.setPWM(2, 0, 0)
  time.sleep(1)
  pwm.setPWM(3, 0, 0)
  time.sleep(1)
  pwm.setPWM(4, 0, 0)
  time.sleep(1)
  turn(0)

#############
# main code

def run_self_test():
  #init i2c
  setup()

  # test top selector positions
  servo = 0
  while(servo < 0):
    select(servo)
    time.sleep(2)
    servo = servo + 1
  select(0)

  # test bottom doors
  servo = 0
  while(servo < 4):
    open(servo)
    print "open"
    time.sleep(3)
    close(servo)
    print "closed"
    time.sleep(3)
    pwm.setPWM(servo+1, 0, 0)
    servo = servo + 1

  # test barrel position
  servo=0
  while(servo < 16):
    rotateTo(servo)
    time.sleep(3)
    servo = servo + 1

  #databas tests
  #load(6,2) #rotation,door
  #time.sleep(5)
  #load(9,2) #rotation,door
  #time.sleep(5)
  #dispense(9,2)
  #dispense(6,2)
  
  #finish test
  GPIO.cleanup()
  exit()

#run_self_test()




parser = argparse.ArgumentParser()
parser.add_argument("-x")
parser.add_argument("-y")
parser.add_argument("-mode")
args = parser.parse_args()
#print args.x
#print args.y

if(args.mode == "vend"):
  sys.stderr.write('vending... \n')
  dispense(int(args.x), int(args.y))
elif(args.mode == "load"):
  sys.stderr.write('loading... \n')
  load(int(args.x), int(args.y))
elif(args.mode == "home"):
  goHome()

GPIO.cleanup()
