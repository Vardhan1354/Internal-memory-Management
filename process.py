class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        self.start = None
        self.end = None
        self.allocated = False

    def allocate(self, start):
        self.start = start
        self.end = start + self.size
        self.allocated = True

    def deallocate(self):
        self.start = None
        self.end = None
        self.allocated = False

    def __str__(self):
        if self.allocated:
            return f"{self.pid}: {self.size} KB [{self.start}-{self.end}]"
        return f"{self.pid}: {self.size} KB [Not Allocated]"