import actions as ac
import comprovations as co
import time
import standingUp as su
import layDown as ld
from ConnectionPlusNavegation import isStandUP


def personaDreta(event, inputQueue):
    # Event where the robot only has to inform the user that they occurred
    if event.event == 'FireAlarm' or event.event == 'Doorbell' or event.event == 'RunningWater' or event.event == 'Rain':
        su.infoEvent(event, inputQueue)

    elif event.event == 'Fall':
        ac.explicacioDeEvent(event)
        su.eventFall(event, inputQueue)

    # Other events
    else:
        ac.explicacioDeEvent(event)
        su.otherEvent(event, inputQueue)



def personaEstirada(event, inputQueue):
    # Ask up to three times preguntarEstat() if there is no reply durint three minutes.
    ac.preguntarEstat()

    # Wait for the user to answer
    answer, userHurt, numInvalidAnswer = co.waitAnswerEstat(inputQueue)

    if answer == 0 or numInvalidAnswer == 5:
        ld.askForHelpLD(inputQueue, event)

    # The user is not hurt
    if answer == 1 and userHurt == 0:

        answer = 0
        # The robot asks the user if they can stand up
        ac.askStandUp()

        # Ask if the user can stand up = 3
        yesNo = co.waitYesNoAnswer(inputQueue, 3)

        if yesNo == 'y':
            # Flag that indicates if the user can stand up on their own
            canStandUp = 1
            time.sleep(1)
            print('\n')
            print("OK")

        if yesNo == 'n':
            # Flag that indicates if the user can stand up on their own
            canStandUp = 0

        # The user can stand up
        if canStandUp == 1:
            # Wait untill the user gets up
            ac.esperarPersonaPeu()
            isStandUP()
            ld.waitStandUp(inputQueue, event)

        # The user can't stand up
        else:

            # The robots asks if it should get close to help the user stand up
            ac.preguntaVolAjuda()

            # Pregunta vol ajuda = 4
            yesNo = co.waitYesNoAnswer(inputQueue, 4)

            # The user wants the robot to get closer to help
            if yesNo == 'y':
                ld.helpStandUp(inputQueue, event)

            # The user doesn't want the robot to get closer
            if yesNo == 'n':
                ld.askForHelpLD(inputQueue, event)

                # The user is hurt
    if answer == 1 and userHurt == 1:
        ld.askForHelpLD(inputQueue, event)
    # TODO: acabar interaccio si la persona esta estirada (fer opcions per terminal o random)