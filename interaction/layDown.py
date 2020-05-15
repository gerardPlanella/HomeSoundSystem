#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import actions as ac
import comprovations as co
import time

EXIT_COMMAND = "exit"

# Every 15 minutes the robot will ask again for help if nobody arrives
quarterHour = 15

def askForHelpLD(inputQueue, event):
    
    # Flag that indicates if someone arrived to help the user
    helpIsHere = 0
    # Count how many times the robot asked for help
    countTimesHelp = 1
    # Flag that indicates if the entered time is an int
    timeCheck = 0
    
    ac.demanarAjuda()
    ac.ferCompanyia()
    
    ac.askNameHelp()
    # Check input from the keyboard
    while inputQueue.qsize() <= 0:
        pass
    
    if inputQueue.qsize() > 0:
        input_str = inputQueue.get()
        nameHelp = input_str
    
        if input_str == EXIT_COMMAND:
            print("Exiting serial terminal.")
            # break
       
        ac.askTimeToHelp(nameHelp)
        
        # Check input from the keyboard
        while inputQueue.qsize() <= 0:
            pass
        
        # Wait untill the time is entered and check it is int()
        timeUntillHelp, timeCheck = co.checkTimeInput(inputQueue, timeCheck, nameHelp)
                    
    # Start time to know how much time passed since the robot asked for help            
    timeStart = time.time()
    
    # Wait untill the help arrives
    while helpIsHere == 0 and timeCheck == 1:
        # Get minutes and seconds since timeStart
        minutes, seconds = co.getWaitTime(timeStart)
        
        # Every 15 minutes ask for help
        if minutes == (quarterHour * countTimesHelp):
            ac.demanarAjuda()
            countTimesHelp += 1
        
        # The person arrived to help the user
        if minutes == timeUntillHelp:
            helpIsHere = 1
            ac.helpArrived(nameHelp, event)
            time.sleep(0.5)
            # END OF TASK #


def waitStandUp(inputQueue, event):

    print('\n')
    print("--------------------------------------------------------")
    print(" ")
    print("User gets up")
    print(" ")
    print("--------------------------------------------------------")
    
    # Ask again if the user is hurt to make sure everything is OK
    ac.preguntarEstat()
    
    # Wait for the user to answer
    answer, userHurt, numInvalidAnswer = co.waitAnswerEstat(inputQueue)
    
    if answer == 0 or (answer == 1 and userHurt == 1) or numInvalidAnswer == 5:
        askForHelpLD(inputQueue, event)
        
    if answer == 1 and userHurt == 0:
        ac.finalProces(event)
        ac.retornInici()

        # END OF TASK #
        
def helpStandUp(inputQueue, event):
    time.sleep(2)
    print('\n')
    print("--------------------------------------------------------")
    print(" ")
    print("The robot gets closer + user stands up")
    print(" ")
    print("--------------------------------------------------------")

    # Ask again if the user is hurt to make sure everything is OK
    ac.preguntarEstat()
    # Wait for the user to answer
    answer, userHurt, numInvalidAnswer = co.waitAnswerEstat(inputQueue)
    
    if answer == 0 or (answer == 1 and userHurt == 1) or numInvalidAnswer == 5:
        askForHelpLD(inputQueue, event)
        
    if answer == 1 and userHurt == 0:
        ac.finalProces(event)
        ac.retornInici()

        # END OF TASK #
