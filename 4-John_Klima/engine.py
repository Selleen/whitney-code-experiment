import numpy as np
import time
import sys
import tkinter as tk
import random
from math import fabs
from const import *

jackImg = np.zeros((5, 16, 16))
jillImg = np.zeros((5, 15, 22))
pailImg = np.zeros((2, 16, 16)) 
hillImg = np.zeros((2, 16, 8)) 
root = tk.Tk()
def timeGetTime():
    return int(round(time.time() * 1000))

def drawSprite(image, position, frame, direction, orientation):
    print(f"Drawing sprite at {position.X}, {position.Y} with frame {frame} and direction {direction}")
    w = 0
    h = 0
    xp = 0
    yp = 0
    clr = 0

    if orientation == 1 or orientation == 3:
        w = len(image[0][0]) * 2
        h = len(image[0]) * 2
    else:
        w = len(image[0]) * 2
        h = len(image[0][0]) * 2

    for Y in range(0, h, 2):
        for X in range(0, w, 2):
            if orientation == 1 or orientation == 3:
                clr = image[frame][Y // 2][X // 2]
            else:
                clr = image[frame][X // 2][Y // 2]

            if clr > 0:
                if direction > 0:
                    xp = position.X + X
                else:
                    xp = position.X + w - X

                if orientation == 0:
                    yp = position.Y - h + Y
                    buffer.PSet(xp, yp, clr)
                elif orientation == 1:
                    yp = position.Y - h + Y
                    buffer.PSet(xp, yp, clr)
                elif orientation == 2:
                    yp = position.Y - Y
                    buffer.PSet(xp, yp, clr)
                elif orientation == 3:
                    yp = position.Y - Y
                    buffer.PSet(xp, yp, clr)
    
def eraseSprite(image, position, frame, direction, orientation):
    print(f"Erasing sprite at {position.X}, {position.Y} with frame {frame} and direction {direction}")
    w = 0
    h = 0
    xp = 0
    yp = 0
    clr = 0

    if orientation == 1 or orientation == 3:
        w = len(image[0][0]) * 2
        h = len(image[0]) * 2
    else:
        w = len(image[0]) * 2
        h = len(image[0][0]) * 2

    for Y in range(0, h, 2):
        for X in range(0, w, 2):
            if orientation == 1 or orientation == 3:
                clr = image[frame][Y // 2][X // 2]
            else:
                clr = image[frame][X // 2][Y // 2]

            if clr > 0:
                if direction > 0:
                    xp = position.X + X
                else:
                    xp = position.X + w - X

                if orientation == 0:
                    yp = position.Y - h + Y
                    buffer.PSet(xp, yp, 0)
                elif orientation == 1:
                    yp = position.Y - h + Y
                    buffer.PSet(xp, yp, 0)
                elif orientation == 2:
                    yp = position.Y - Y
                    buffer.PSet(xp, yp, 0)
                elif orientation == 3:
                    yp = position.Y - Y
                    buffer.PSet(xp, yp, 0)

def PauseTheHill(person):
    print(f"Pausing {person} on the hill.")
    eraseSprite(person.Graphic, person.position, person.Frame, person.direction, person.orientation)
    person.Frame = 2

def MoveUpTheHill(jack, jill):
    print(f"Moving {jack} and {jill} up the hill.")
    eraseSprite(jack.Graphic, jack.position, jack.Frame, jack.direction, jack.orientation)
    jack.orientation = 0
    if jill.position.X > jack.position.X:
        collide = abs(jack.position.X + 6 - jill.position.X + 6)
    else:
        collide = 100
    
    if jack.position.X + 6 < 700 and collide > 16:
        jack.position.X += 6
        jack.direction = 1 
        calculateY(jack) 
    else:
        jack.Frame = 2  

def MoveDownTheHill(jack, jill):
    print(f"Moving {jack} and {jill} down the hill.")
    eraseSprite(jack.Graphic, jack.position, jack.Frame, jack.direction, jack.orientation)
    jack.orientation = 0
    if jill.position.X < jack.position.X:
        collide = abs(jack.position.X - 6 - jill.position.X - 6)
    else:
        collide = 100
    if jack.position.X - 6 > 30 and abs(collide) > 16:
        jack.position.X = jack.position.X - 6 
        jack.direction = 0
        calculateY(jack)
    else:
        jack.Frame = 2

def FellDown(person):
    print(f"{person} fell down!")
    eraseSprite(person.Graphic, person.position, person.Frame, person.direction, person.orientation)
    person.orientation = 3
    person.Frame = 3
    drawSprite(person.Graphic, person.position, person.Frame, person.direction, person.orientation)

def BrokeCrown(person):
    print(f"{person} broke their crown!")
    eraseSprite(person.Graphic, person.position, person.Frame, person.direction, person.orientation)
    person.orientation = 3
    person.Frame = 4
    drawSprite(person.Graphic, person.position, person.Frame, person.direction, person.orientation)

def TumblingThem(jack, jill):
    print(f"Tumbling {jack} and {jill}.")
    eraseSprite(jack.Graphic, jack.position, jack.Frame, jack.direction, jack.orientation)
    jack.orientation = (jack.orientation + 1) % 4  

    if jill.position.X < jack.position.X:
        collide = abs(jack.position.X - 6 - jill.position.X - 6)
    else:
        collide = 100
    

    if jack.position.X - 6 > 30 and abs(collide) > 16:
        jack.position.X -= 6 
        jack.direction = 0
        calculateY(jack)
    else:
        jack.position.X -= 6  
        jack.direction = 0  
        calculateY(jack) 
        
        eraseSprite(jill.Graphic, jill.position, jill.Frame, jill.direction, jill.orientation)
        
        jill.EmotionalState = jack.EmotionalState
        jill.Frame = 4
        
        if jack.position.X < 0:
            reset()

def drawHill():
    sx = 0
    sy = 300 - len(hillImg[0]) * 4  # bottom to top
    w = len(hillImg[0]) 
    h = len(hillImg[1]) 
    pos = Vector()

    buffer.drawWidth = 2

    for X in range(w * 2, 800 - (w * 4), (w * 2) + 2):
        sy = sy - 4
        pos.X = X
        pos.Y = sy
        drawSprite(hillImg, pos, 0, 1, 0)

    pos.Y = pos.Y - h * 2 - 3
    drawSprite(pailImg, pos, 0, 1, 0)

def reset():
    jack.EmotionalState = INDECISIVE
    jill.EmotionalState = INDECISIVE

    SetOptions()

    if YourAttitude == CHAUVINIST:
        PlaceJackAndJill(jack, jill)
    else:
        PlaceJackAndJill(jill, jack)

def PlaceJackAndJill(lead, follow):
    lead.direction = 1
    lead.orientation = 0
    lead.width = len(lead.Graphic[0]) * 2
    lead.position['X'] = 68
    calculateY(lead)

    follow.direction = 1
    follow.orientation = 0
    follow.width = len(follow.Graphic[0]) * 2
    follow.position['X'] = 32
    calculateY(follow)

    buffer_cls()
    drawHill()

def calculateY(targ):
    # y is *ALWAYS* a function of x
    fw = targ.position['X'] + targ.width
    targ.position['Y'] = 254 - 4 * (fw - (fw % 32)) // 32

def Form_Unload():
    sys.exit()

def SetOptions():
    Attitude_Click[0].Value = True
    JacksDesire_Click[1].Value = True
    JillsDesire_Click[1].Value = True
    Allure_Click[1] = True
    
def Attitude_Click(Index):
    global YourAttitude
    if Index == 0:
        PlaceJackAndJill(jack, jill)
        YourAttitude = CHAUVINIST
    else:
        PlaceJackAndJill(jill, jack)
        YourAttitude = FEMINIST

def JacksDesire_Click(Index):
    if Index == 0:
        jack.Desire = 0
    elif Index == 1:
        jack.Desire = 0.5
    elif Index == 2:
        jack.Desire = 1

def JillsDesire_Click(Index):
    if Index == 0:
        jill.Desire = 0
    elif Index == 1:
        jill.Desire = 0.5
    elif Index == 2:
        jill.Desire = 1

def Allure_Click(Index):
    if Index == 0:
        pail.Allure = 0
    elif Index == 1:
        pail.Allure = 0.5
    elif Index == 2:
        pail.Allure = 1

def Form_Load():
    random.seed()  # Randomize Timer equivalent
    
    placeWindow() 

    ParseImage(jackImg, jack1, 0)
    ParseImage(jackImg, jack2, 1)
    ParseImage(jackImg, jack3, 2)
    ParseImage(jackImg, jack4, 3)
    ParseImage(jackImg, jack5, 4)

    ParseImage(jillImg, jill1, 0)
    ParseImage(jillImg, jill2, 1)
    ParseImage(jillImg, jill3, 2)
    ParseImage(jillImg, jill4, 3)
    ParseImage(jillImg, jill5, 4)

    ParseImage(pailImg, pail1, 0)
    ParseImage(hillImg, hill, 0)

    jack.Graphic = jackImg
    jill.Graphic = jillImg
    pail.Graphic = pailImg

    SetOptions()

def ParseImage(tarray, ttext, ti):
    w = len(tarray[0])
    h = len(tarray[1])

    for Y in range(h):
        for X in range(w):
            v = ttext[(w + 1) * Y + X]
            tarray[ti][X][Y] = FindColorValue(v)

def FindColorValue(tv):
    if tv == "O":
        return OV
    elif tv == "A":
        return AV
    elif tv == "B":
        return BV
    elif tv == "C":
        return CV
    elif tv == "D":
        return DV
    elif tv == "E":
        return EV
    elif tv == "F":
        return FV
    elif tv == "G":
        return GV
    elif tv == "H":
        return HV
    elif tv == "I":
        return IV
    elif tv == "J":
        return JV
    return None  # Default case if no match

def placeWindow():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 800
    window_height = 600

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.place(x=0, y=0)
    buffer = canvas

    return root, buffer

def Draw():
    global jack, jill, fc

    if jack.EmotionalState == INDECISIVE:
        PauseTheHill(jack)
    elif jack.EmotionalState == WILLING:
        MoveUpTheHill(jack, jill)
    elif jack.EmotionalState == RELUCTANT:
        MoveDownTheHill(jack, jill)
    elif jack.EmotionalState == FALLING:
        FellDown(jack)
    elif jack.EmotionalState == BROKE_CROWN:
        BrokeCrown(jack)
    elif jack.EmotionalState == TUMBLING:
        TumblingThem(jack, jill)

    if jill.EmotionalState == INDECISIVE:
        PauseTheHill(jill)
    elif jill.EmotionalState == WILLING:
        MoveUpTheHill(jill, jack)
    elif jill.EmotionalState == RELUCTANT:
        MoveDownTheHill(jill, jack)
    elif jill.EmotionalState == FALLING:
        FellDown(jill)
    elif jill.EmotionalState == BROKE_CROWN:
        BrokeCrown(jill)
    elif jill.EmotionalState == TUMBLING:
        TumblingThem(jill, jack)

    d = timeGetTime()

    drawSprite(jackImg, jack.position, jack.Frame, jack.direction, jack.orientation)
    drawSprite(jillImg, jill.position, jill.Frame, jill.direction, jill.orientation)

    # The_Picture.Picture = buffer.Image

    t = int(fabs(timeGetTime() - d))

    fc += t
    if fc > 100:
        fc = 0

        eraseSprite(jackImg, jack.position, jack.Frame, jack.direction, jack.orientation)
        eraseSprite(jillImg, jill.position, jill.Frame, jill.direction, jill.orientation)

        jack.Frame += 1
        if jack.Frame > 1:
            jack.Frame = 0

        jill.Frame += 1
        if jill.Frame > 1:
            jill.Frame = 0

# Example
jack = Person()
jill = Person()

jack.EmotionalState = WILLING
jill.EmotionalState = RELUCTANT

fc = 0

