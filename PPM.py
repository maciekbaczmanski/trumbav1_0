import RPi.GPIO as GPIO
import time

servoPIN1 = 21
servoPIN2 = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
p1 = GPIO.PWM(servoPIN1, 500)  # GPIO 17 for PWM with 50Hz
p1.start(99)  # Initialization
p2 = GPIO.PWM(servoPIN2, 500)  # GPIO 17 for PWM with 50Hz
p2.start(30)  # Initialization

try:
    while True:

        p1.ChangeDutyCycle(99)
        p1.ChangeDutyCycle(30)
        time.sleep(0.5)
        # p.ChangeDutyCycle(7.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(10)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(12.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(10)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(7.5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(5)
        # time.sleep(0.5)
        # p.ChangeDutyCycle(2.5)
        # time.sleep(0.5)
except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()
