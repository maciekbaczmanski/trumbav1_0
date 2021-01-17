import time



class battery:

    def __init__(self):
        self.power = 100
        self.powertospeed = 100
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global power
        while self._running:
            time.sleep(0.5) #Five second delay
            if self.power > 0:
                self.power = self.power - 1
            if 10 % self.power == 0:
                self.powertospeed = self.power
            print(self.power)