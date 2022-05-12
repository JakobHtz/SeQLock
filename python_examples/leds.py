import RPi.GPIO as GPIO
import time

green = 11
yellow = 13
red = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

try:
    while (True):
        print("True")
        GPIO.output(red,GPIO.HIGH)
        GPIO.output(yellow,GPIO.HIGH)
        GPIO.output(green,GPIO.HIGH)
        time.sleep(1)
        print("False")
        GPIO.output(red,GPIO.LOW)
        GPIO.output(yellow,GPIO.LOW)
        GPIO.output(green,GPIO.LOW)
        time.sleep(1)
finally:
    GPIO.cleanup()
