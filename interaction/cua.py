
classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater','Silence']

class event():

   def __init__ (self, loc1, e1 , timestamp, confidence):
      global classLabels
      self.event = classLabels[e1]
      self.lloc = loc1
      self.timeestamp = timestamp
      self.confidence = confidence
      if classLabels[e1] == "Rain":
          self.priority = 1 * self.confidence
      elif classLabels[e1] == "Doorbell":
          self.priority = 2 * self.confidence
      elif classLabels[e1] == "BoilingWater":
          self.priority = 3 * self.confidence
      elif classLabels[e1] == "RunningWater":
          self.priority = 4 * self.confidence
      elif classLabels[e1] == "HeavyBreath":
          self.priority = 5 * self.confidence
      elif classLabels[e1] == "CutleryFall":
          self.priority = 6 * self.confidence
      elif classLabels[e1] == "GlassBreak":
          self.priority = 7 * self.confidence
      elif classLabels[e1] == "FireAlarm":
          self.priority = 8 * self.confidence
      elif classLabels[e1] == "Fall":
          self.priority = 9 * self.confidence
      elif classLabels[e1] == "Complain":
          self.priority = 10 * self.confidence
      else :
          self.priority = 11 * self.confidence

class ListaEvents():

    def __init__(self):
        self.listaEvents = []

    def bubbleSort(self):
        #self.listaEvents.sort(key=)
        n = len(self.listaEvents)
         # Traverse through all array elements
        for i in range(n):
        # Last i elements are already in place
            for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
                if self.listaEvents[j].priority > self.listaEvents[j + 1].priority:
                    self.listaEvents[j], self.listaEvents[j + 1] = self.listaEvents[j + 1], self.listaEvents[j]
        self.listaEvents.reverse()


    def appendEvent (self, event):
        trobat = 0
        for event_aux in self.listaEvents:
            if event.event == event_aux.event:
                trobat = 1
                if event.priority > event_aux.priority:
                    self.listaEvents.remove(event_aux)
                    self.listaEvents.append(event)

        if trobat == 0:
            self.listaEvents.append(event)
        self.bubbleSort()

    def eventRemove(self, event):
        self.listaEvents.remove(event)

    def popEvent (self):
        return self.listaEvents[0]

    def anyList(self):
        return len(self.listaEvents)

    def printLista (self):
        for e in self.listaEvents:
            print(e.event, e.priority)