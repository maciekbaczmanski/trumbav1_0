import RPi.GPIO as GPIO
import time

# washerpwm = None
amotor = None
bmotor = None
current_speed_a = 0
current_speed_b = 0
p1 = None
p2 = None

def GPIO_Setup():
    global amotor, bmotor, current_speed_a, current_speed_b, p1,p2
    # global washerpwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(26, GPIO.OUT)  # red
    GPIO.setup(19, GPIO.OUT)  # yellow1
    GPIO.setup(13, GPIO.OUT)  # yellow2
    GPIO.setup(6, GPIO.OUT)  # yellow3
    GPIO.setup(5, GPIO.OUT)  # green
    GPIO.setup(22, GPIO.OUT)  # APWM
    GPIO.setup(17, GPIO.OUT)  # A1
    GPIO.setup(27, GPIO.OUT)  # A2
    GPIO.setup(2, GPIO.OUT)  # BPWM
    GPIO.setup(4, GPIO.OUT)  # B1
    GPIO.setup(3, GPIO.OUT)  # B2
    # GPIO.setup(20, GPIO.OUT)  # p1
    GPIO.setup(21, GPIO.OUT)  # szczotki
    gpioout(21, True)
    amotor = GPIO.PWM(22, 100000)
    bmotor = GPIO.PWM(2, 100000)
    GPIO.setup(23, GPIO.OUT)
    amotor.start(current_speed_a)
    bmotor.start(current_speed_b)
    GPIO.setup(24, GPIO.IN)
    time.sleep(0.02)
    GPIO.output(23, False)  # do odl
    # p1 = GPIO.PWM(20, 500)  # GPIO 17 for PWM with 50Hz
    # p1.start(99)
    #
    # p2 = GPIO.PWM(21, 500)  # GPIO 17 for PWM with 50Hz
    # p2.start(30)
    time.sleep(0.1)

    # p1.ChangeDutyCycle(99)
    # p2.ChangeDutyCycle(30)

# def keepalive():
#     global p1, p2
#     p1.ChangeDutyCycle(99)
#     p2.ChangeDutyCycle(30)

def a_dir(dir):
    if dir:
        gpioout(17, True)
        gpioout(27, False)
    else:
        gpioout(17, False)
        gpioout(27, True)


def b_dir(dir):
    if dir:
        gpioout(3, True)
        gpioout(4, False)
    else:
        gpioout(3, False)
        gpioout(4, True)


def gpioout(pin, state):
    GPIO.output(pin, state)


def change_a_speed(speed):
    global amotor, current_speed_a
    current_speed_a = speed
    amotor.ChangeDutyCycle(speed)


def change_b_speed(speed):
    global bmotor, current_speed_b
    current_speed_b = speed
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
