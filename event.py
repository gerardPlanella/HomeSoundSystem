
class event ():

   def __init__ (self, e1, loc1, timestamp, confidence):
      self.event = e1
      self.lloc = loc1
      self.timeestamp = timestamp
      self.confidence = confidence
      if e1 == "Rain" :
          self.priority = 1 * self.confidence
      elif e1 == "Doorbell sound" :
          self.priority = 2 * self.confidence
      elif e1 == "Water boiling" :
          self.priority = 3 * self.confidence
      elif e1 == "Water running" :
          self.priority = 4 * self.confidence
      elif e1 == "Heavy breath" :
          self.priority = 5 * self.confidence
      elif e1 == "Knives/ forks/Spoon falling to the floor":
          self.priority = 6 * self.confidence
      elif e1 == "Glass breaking":
          self.priority = 7 * self.confidence
      elif e1 == "Fire alarm system":
          self.priority = 8 * self.confidence
      elif e1 == "Person falling ":
          self.priority = 9 * self.confidence
      elif e1 == "Complain /Scream":
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
                    self.listaEvents[j].priority, self.listaEvents[j + 1].priority = self.listaEvents[j + 1].priority, self.listaEvents[j].priority
        self.listaEvents.reverse()


    def appendEvent (self, event):
        self.listaEvents.append(event)

    def popEvent (self):
        return self.listaEvents.pop(0)

    def printLista (self):
        for e in self.listaEvents:
            print(e.event, e.priority)


llista = ListaEvents()

obj1 = event("Rain", "cuina", 3, 0.90)

obj2 = event("Person falling", "cuina", 3, 0.90)

obj3 = event("Glass breaking", "cuina", 3, 0.90)

obj4 = event("Heavy breath", "cuina", 3, 0.90)

obj5 = event("Complain /Scream", "cuina", 3, 0.90)

llista.appendEvent(obj1)
llista.appendEvent(obj2)
llista.appendEvent(obj3)
llista.appendEvent(obj4)
llista.appendEvent(obj5)

llista.bubbleSort()

llista.printLista()











