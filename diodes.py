import RPi.GPIO as GPIO
import time

# washerpwm = None
amotor = None
bmotor = None
def GPIO_Setup():
    global amotor,bmotor
    # global washerpwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)  # red
    GPIO.setup(19, GPIO.OUT)  # yellow1
    GPIO.setup(13, GPIO.OUT)  # yellow2
    GPIO.setup(6, GPIO.OUT)  # yellow3
    GPIO.setup(5, GPIO.OUT)  # green
    GPIO.setup(21, GPIO.OUT)  # gąbka
    GPIO.setup(22, GPIO.OUT)  # APWM
    GPIO.setup(17, GPIO.OUT)  # A1
    GPIO.setup(27, GPIO.OUT)  # A2
    GPIO.setup(2, GPIO.OUT)  # BPWM
    GPIO.setup(4, GPIO.OUT)  # B1
    GPIO.setup(3, GPIO.OUT)  # B2
    washerpwm = GPIO.PWM(21, 1000000)
    washerpwm.start(0.0005)
    amotor = GPIO.PWM(2, 100000)
    bmotor = GPIO.PWM(3, 100000)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.IN)
    time.sleep(0.02)
    GPIO.output(23, False)
    amotor.start(0)
    bmotor.start()


def gpioout(pin, state):
    GPIO.output(pin, state)

def change_a_speed(speed):
    global amotor
    amotor.ChangeDutyCycle(speed)

def change_b_speed(speed):
    global bmotor
    bmotor.ChangeDutyCycle(speed)

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
