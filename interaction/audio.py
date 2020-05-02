#!/usr/bin/env python
# -*- coding: utf-8 -*-

#hola guapa


import pyttsx3

class speech():
    def __init__(self):
        self.engine = pyttsx3.init()
        print(self.engine.getProperty('voice'))
        self.engine.setProperty('rate', 170)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)


    # It's just a text to speech function..
    def reproduceText(self, somethingToSay):
        self.engine.say(somethingToSay)
        self.engine.runAndWait()
        #self.engine.stop()
        return 0

