class Counter:
    counter = 0
    start_time = 0

    def __init__(self):
        pass

    def increment(self):
        self.counter += 1

    def reset(self):
        self.counter = 0

    def change_start(self, start):
        self.start_time = start


count = Counter()

