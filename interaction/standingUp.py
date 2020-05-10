#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import actions as ac
import comprovations as co
import time

EXIT_COMMAND = "exit"

# Every 15 minutes the robot will ask again for help if nobody arrives
quarterHour = 15

def askForHelpSU(inputQueue, event):
    
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


def eventFall(event, inputQueue):
    
    ac.askFall()
                        
    # Ask Fall = 2
    yesNo = co.waitYesNoAnswer(inputQueue, 2)
    
    # The user did fall and got back up
    if yesNo == 'y':
        # Ask if the user is hurt
        ac.preguntarEstat()
        
        # Wait for the user to answer
        answer, userHurt = co.waitAnswerEstat(inputQueue)
        
        # The user did not reply and the robot has to ask for help
        # Or the answer is that they are hurt
        if answer == 0 or (answer == 1 and userHurt == 1):

            askForHelpSU(inputQueue, event)
        
        # The user is not hurt
        if answer == 1 and userHurt == 0:
            ac.finalProces(event)
            ac.retornInici()

            # END OF TASK #
    
    # The user didn't fall
    if yesNo == 'n':
        ac.falseAlarm()
        ac.finalProces(event)
        ac.retornInici()

        # END OF TASK #
        
        
def otherEvent(event, inputQueue):
    # Ask if the event happened
    ac.askEventHappened()
    
    # Ask if the event happened = 1
    yesNo = co.waitYesNoAnswer(inputQueue, 1)
    
    # THe event did happen
    if yesNo == 'y':
        
        # The robot asks if the user is OK to make sure
        ac.preguntarEstat()
    
        # Wait for the user to answer
        answer, userHurt = co.waitAnswerEstat(inputQueue)
        
        # The user did not reply and the robot has to ask for help
        # Or the answer is that they are hurt
        if answer == 0 or (answer == 1 and userHurt == 1):

            askForHelpSU(inputQueue, event)
        
        # The user is not hurt
        if answer == 1 and userHurt == 0:
            ac.finalProces(event)
            ac.retornInici()

            # END OF TASK #
    
    # The event didn't happen
    if yesNo == 'n':
        ac.falseAlarm()
        ac.finalProces(event)
        ac.retornInici()

        # END OF TASK #
        
        
def infoEvent(event):
    # The robot explains why it is moving arround
    ac.explicacioDeEventInfo(event)
    ac.finalProces(event)
    ac.retornInici()

    # END OF TASK #