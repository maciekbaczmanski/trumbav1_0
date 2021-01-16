import RPi.GPIO as GPIO

# washerpwm = None

def GPIO_Setup():
    # global washerpwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)    #red
    GPIO.setup(19, GPIO.OUT)    #yellow1
    GPIO.setup(13, GPIO.OUT)    #yellow2
    GPIO.setup(6, GPIO.OUT)    #yellow3
    GPIO.setup(5, GPIO.OUT)    #green
    GPIO.setup(21, GPIO.OUT)    #gąbka
    washerpwm = GPIO.PWM(21, 1000000)
    washerpwm.start(0.0005)


def charge_to_diode(percent):
    GPIO.output(26, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)
    GPIO.output(5, False)

    percent = int(percent)
    if percent == 0:
        GPIO.output(26, False)
        GPIO.output(19, False)
        GPIO.output(13, False)
        GPIO.output(6, False)
        GPIO.output(5, False)
    elif percent > 0 and percent <= 20:
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