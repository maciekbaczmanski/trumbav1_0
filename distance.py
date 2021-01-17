import RPi.GPIO as GPIO
import time

class distance:

    def __init__(self):
        self.dist = 100
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:

            GPIO.output(23, True)
            time.sleep(0.00001)
            GPIO.output(23, False)
            measurement = True
            lastinp = GPIO.input(24)
            testtime = time.time()
            error = False
            while measurement:
                inp = GPIO.input(24)
                if abs(testtime - time.time()) > 0.1:
                    error = True
                    break
                if inp and not lastinp:
                    start_time = time.time()

                elif lastinp and not inp:
                    end_time = time.time()
                    measurement = False
                lastinp = inp
            # while GPIO.input(24) == 0:
            #     start_time = time.time()
            # while GPIO.input(24) == 1:
            #     end_time = time.time()
            time.sleep(0.1)
            if not error:
                time1 = end_time - start_time
                self.dist = 17150 * time1
            else:
                self.dist = 0
            # print(self.dist)
