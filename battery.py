import time


class battery:

    def __init__(self):
        self.power = 100
        self.powertospeed = 100
        self._running = True
        self.count = False

    def terminate(self):
        self._running = False

    def run(self):
        global power
        while self._running:
            time.sleep(0.5)  # Five second delay
            if self.power > 0 and self.count:
                self.power = self.power - 1
            if 20 < self.power <= 50:
                self.powertospeed = 99
            elif self.power <= 20:
                self.powertospeed = 0
            # print(self.power)

    def add_power(self, new_power):

        self.power += new_power

        if self.power > 100:
            self.power = 100
        if self.power>50:
            self.powertospeed = 100
        elif 20 < self.power <= 50:
            self.powertospeed = 99
        elif self.power <= 20:
            self.powertospeed = 0