import threading
import socket
import actions as ac
from Navegation import navegation
from poseConnection import posseConnection
import time


def NavegationStarts(event):
    nav = navegation()
    ok = nav.startNavegation()
    if ok == True:
        print("\nThe robot moves towards ", event.lloc, "\n")
        ac.StartMoving(event.lloc)
        navOK = nav.goSomewhere(event.lloc)
        nav.close()
        return navOK
    else:
        print("We haven't been able to connect to the robot's navigation")
        return ok

def NavegationEnd():
    nav = navegation()
    ok = nav.startNavegation()
    if ok == True:
        print("The robot goes to the resting point\n")
        ac.StartMoving("restingPoint")
        navOK = nav.goSomewhere("restingPoint")
        nav.close()
        if navOK == "OK":
            print("The robot arrives to the resting point\n")
        elif navOK == "KO":
            print("The robot cannot arrive to the resting point\n")
    else:
        print("We haven't been able to connect to the robot's navigation")
        return ok



def SearchForPerson(pose):
    # connexio amb el arroyo
    poseOK = pose.startPoseConnnection()
    if poseOK:
        persona = pose.person()
        if persona == "yes":
            return persona
        else:
            # connexio amb la navegacio
            nav = navegation()
            ok = nav.startNavegation()
            turn = "OK"
            if ok:
                while turn == "OK":
                    persona = pose.person()
                    if persona == "yes":
                        return persona
                    turn = nav.turn()
                pose.close()
                pose.delete()
                nav.close()
                return persona
            else:
                pose.close()
                pose.delete()
                return persona
    else:
        print("we can't connect to the pose detection")
        return "KO"

def askPose(pose):
    position = pose.position()
    pose.close()
    pose.delete()
    return position

def isStandUP():
    pose = posseConnection()
    persona = pose.person()
    if persona == "yes":
        position = pose.position()
        while position != "dret" or position != "sentat":
            time.sleep(60)
            position = pose.position()

    else:
        print("we can't connect to the pose detection ---> start a simulation")

