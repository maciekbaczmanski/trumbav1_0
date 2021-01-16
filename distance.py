import RPi.GPIO as GPIO
import time




while True:
    GPIO.output(23, True)
    time.sleep(0.00001)
    GPIO.output(23, False)
    while GPIO.input(24) == 0:
        start_time = time.time()
    while GPIO.input(24) == 1:
        end_time = time.time()
    time.sleep(0.1)
    time1 = end_time - start_time
    distance = 17150 * time1
    print("Measured Distance is:", distance, "cms.")
