#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import actions as ac


# Every 15 minutes the robot will ask again for help if nobody arrives
quarterHour = 15
timeRepeatQuestion1 = 30
timeRepeatQuestion2 = [1, 15]
timeRepeatQuestion3 = [2, 0]

EXIT_COMMAND = "exit"

# Wait for the user to answer if they are hurt
def waitAnswerEstat(inputQueue):
    
    # Time when the first question is made (Are you hurt?)
    timeStart = time.time()
    # Count how many times the robot asks if the person is hurt
    i = 0
    # Flag that indicates if the user has given an answer
    answer = 0
    # Flag that indicates if the user is heart (1 = yes, 0 = no)
    userHurt = 0
    
    while i < 3:
        # Check input from the keyboard
        if inputQueue.qsize() > 0:
            input_str = inputQueue.get()
            answer = 1
        
            if input_str == EXIT_COMMAND:
                print("Exiting serial terminal.")
                break
            
            # The answer is yes --> they are hurt  
            if input_str == 'y':
                userHurt = 1
                i = 4
            
            # The answer is no --> they are not hurt 
            elif input_str == 'n':
                userHurt = 0
                i = 4
            
            else:
                print('\n')
                print(input_str + " is an invalid answer")
                answer = 0
                i = 0
                timeStart = time.time()
                ac.preguntarEstat()
            
        # Count time with no answer from the user
        if answer == 0:
            # Get minutes and seconds since timeStart
            minutes, seconds = getWaitTime(timeStart)
            
            if minutes == timeRepeatQuestion3[0] and seconds >= timeRepeatQuestion3[1] :
                print('\n')
                print("Three minutes passed with no answer.")
                i += 1
            elif i == 1 and minutes == timeRepeatQuestion2[0] and seconds >= timeRepeatQuestion2[1]:
                i += 1
                ac.preguntarEstat()
            elif i == 0 and seconds > timeRepeatQuestion1:
                i += 1
                ac.preguntarEstat()
                
    return answer, userHurt


# Get hours, minutes and seconds since timeStart
def getWaitTime(timeStart):
    
    # Get the time waiting for answer
    timeEnd = time.time()
    elapsedTime = timeEnd - timeStart
    hours = elapsedTime // 3600
    elapsedTime = elapsedTime - 3600 * hours
    minutes = elapsedTime // 60
    seconds = elapsedTime - (60 * minutes)
    
    return minutes, seconds


def checkTimeInput(inputQueue, timeCheck, nameHelp):

    while timeCheck == 0:
        if inputQueue.qsize() > 0:
            input_str = inputQueue.get()
    
            if input_str == EXIT_COMMAND:
                print("Exiting serial terminal.")
                break
            
            try:
                int(input_str)
                timeCheck = 1
                timeUntillHelp = int(input_str)
                print('\n')
                print("OK")
                print("(>> Waiting for the help to arrive <<)")
                
            except:
                print('\n')
                print(input_str + " is an invalid answer")
                ac.askTimeToHelp(nameHelp)
                
    return timeUntillHelp, timeCheck

def waitYesNoAnswer(inputQueue, question):
    
    answer = 0
    
    # Check input from the keyboard
    while inputQueue.qsize() <= 0:
        pass
    
    while answer == 0:
        if inputQueue.qsize() > 0:
            input_str = inputQueue.get()
    
            if input_str == EXIT_COMMAND:
                print("Exiting serial terminal.")
                break
            
            # The answer is yes           
            if input_str == 'y':
                return 'y'
                        
            # The answer is no
            elif input_str == 'n':
                return 'n'
            
            else:
                answer = 0
                print('\n')
                print(input_str + " is an invalid answer")
                if question == 1:
                    ac.askEventHappened()
                if question == 2:
                    ac.askFall()
                if question == 3:
                    ac.askStandUp()
                if question == 4:
                    ac.preguntaVolAjuda()
                



