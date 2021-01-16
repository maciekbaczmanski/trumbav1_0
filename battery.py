import time



class battery:

    def __init__(self):
        self.power = 100
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global power
        while self._running:
            time.sleep(5) #Five second delay
            self.power = self.power - 10