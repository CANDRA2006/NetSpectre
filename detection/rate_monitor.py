import time

class RateMonitor:
    def __init__(self):
        self.start_time = time.time()

    def calculate_rate(self, total_ports):
        duration = time.time() - self.start_time
        if duration == 0:
            return 0
        return round(total_ports / duration, 2)