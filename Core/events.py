from datetime import datetime

class threadInfo():
    __slots__ = ["running", "events"]

    def __init__(self):
        self.running = True
        self.events = []

    def setRun(self, running):
        self.running = running

    def getRun(self):
        return self.running

    def getEvent(self):
        return self.events.pop(0)

    def addEvent(self, event):
        self.events.append(event)

    def nEvents(self)
        return len(self.events)


class event():
    __slots__ = ["time", "type", "location", "id"]

    def __init__ (self, type, location):
        self.time = datetime.now()
        self.type = type
        self.location = location

    def time2str(self):
         return self.time.strftime("%H:%M:%S")

    def resetTime(self):
        self.time = datetime.now()
