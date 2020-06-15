import threading
import socket
import actions as ac
from Navegation import navegation
from poseConnection import posseConnection
import time

places = ["livingroom", "bedroom", "kitchen", "bathroom"]


def NavegationStarts(event):
    nav = navegation()
    ok = nav.thread_function_SERVERCONNAV()
    if ok == True:
        print("\nThe robot moves towards ", event.lloc, "\n")
        ac.StartMoving(event.lloc)
        navOK = nav.goSomewhere(event.lloc)
        print("navegation starts ", navOK)
        nav.close()
        return navOK
    else:
        print("We haven't been able to connect to the robot's navigation")
        return ok

def NavegationEnd():
    nav = navegation()
    ok = nav.thread_function_SERVERCONNAV()
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

def searchForSomeone(event):
    nav = navegation()
    ok = nav.thread_function_SERVERCONNAV()
    pose = posseConnection()
    print("abans start pose connection")
    poseOK = pose.thread_function_SERVERCONPOSE()
    print("despres start pose connection")
    if ok == True:
        for place in places:
            if place != event.lloc:
                navOK = nav.goSomewhere(place)
                if navOK == "OK":
                    if poseOK:
                        persona = pose.person()
                        if persona == "yes":
                            return persona
                        else:
                            turn = "OK"
                            while turn == "OK":
                                persona = pose.person()
                                if persona == "yes":
                                    return "OK"
                                turn = nav.turn()
                    else:
                        print("we can't connect to the pose detection")
                        return "KO"
                else:
                    print("The robot cannot arrive to the resting point\n")
                    return "KO"
            print ("cambio de lloc *****************************************************")
        pose.close()
        pose.delete()
        nav.close()
        return "KO"
    else:
        print("We haven't been able to connect to the robot's navigation")
        return "KO"

def SearchForPerson(pose):
    # connexio amb el arroyo
    poseOK = pose.thread_function_SERVERCONPOSE()
    if poseOK:
        persona = pose.person()
        if persona == "yes":
            return persona
        else:
            # connexio amb la navegacio
            nav = navegation()
            ok = nav.thread_function_SERVERCONNAV()
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
                nav.close()
                pose.close()
                pose.delete()
                return persona
    else:
        print("we can't connect to the pose detection")
        pose.close()
        pose.delete()
        return "KO"

def askPose(pose):
    position = pose.position()
    pose.close()
    pose.delete()
    return position

def isStandUP():
    pose = posseConnection()
    pose.thread_function_SERVERCONPOSE()
    persona = pose.person()
    if persona == "yes":
        position = pose.position()
        while position == "estirat":
            time.sleep(15)
            position = pose.position()
            print("posicion ", position)
        pose.close()
    else:
        print("we can't connect to the pose detection ---> start a simulation")
        pose.close()

