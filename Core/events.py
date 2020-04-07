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

    def nEvents(self):
        return len(self.events)


class Event():
    __slots__ = ["time", "type", "location", "id", "confidence"]

    def __init__ (self, event_type, location, confidence):
        self.time = datetime.now()
        self.type = event_type
        self.location = location
        self.confidence = confidence

    def time2str(self):
         return self.time.strftime("%H:%M:%S")

    def resetTime(self):
        self.time = datetime.now()
