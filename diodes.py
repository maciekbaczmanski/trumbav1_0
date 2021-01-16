import RPi.GPIO as GPIO

def GPIO_Setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)    #red
    GPIO.setup(19, GPIO.OUT)    #yellow1
    GPIO.setup(13, GPIO.OUT)    #yellow2
    GPIO.setup(6, GPIO.OUT)    #yellow3
    GPIO.setup(5, GPIO.OUT)    #green

def charge_to_diode(percent):
    GPIO.output(26, False)
    GPIO.output(19, False)
    GPIO.output(23, False)
    GPIO.output(6, False)
    GPIO.output(5, False)

    if percent <= 20:
        GPIO.output(26, True)
    elif percent > 20 and percent <= 40:
        GPIO.output(26, True)
        GPIO.output(19, True)
    elif percent > 40 and percent <= 60:
        GPIO.output(26, True)
        GPIO.output(19, True)
        GPIO.output(13, True)
    elif percent > 60 and percent <= 80:
        GPIO.output(26, True)
        GPIO.output(19, True)
        GPIO.output(13, True)
        GPIO.output(6, True)
    else:
        GPIO.output(26, True)
        GPIO.output(19, True)
        GPIO.output(13, True)
        GPIO.output(6, True)
        GPIO.output(5, True)