import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import subprocess
import pdb

# append in windows for subprocess to work
cmd='cmd /C'

#Append extension such as screen1.png
screenShot="adb shell screencap sdcard/screen"
pull="adb pull /sdcard/screen"

#Default templates for matching
templateMonster="templateCavernicola.png"
templateSign="templateSign.png"
pondBottom="pondtemplate.png"

def runAdbCommand(command):
    proc = subprocess.Popen([cmd+str(command)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    print(str(stdout.decode('utf-8')))
    print(str(stderr.decode('utf-8')))

def pressScreen(timeForLongPress):
    #Time is sent in ms
    #set coordenates properly ()
    longPressCmd="adb shell input touchscreen swipe 1000 1000 1000 1000 "+str(timeForLongPress)
    runAdbCommand(longPressCmd)


def matchTwoTemplates(image,):


    #Image read and transform
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)[1785:,:]
    img_gray[img_gray>20]=255
    img_gray[img_gray<=20]=0
    # Find indices where the condition is met
    indices = np.where(img_gray == 0)

    # sort by y first then x
    sorted_indices = sorted(indices[0])
    result = sorted_indices[-1]
    lineThickness = 2
    cv2.line(img_gray, (0, result), (1440, result), 0, lineThickness)
    return result

while(True):

    #Factor for long press dists under 550
    factor=0.35
    #Factor for long press dists over 550
    factorOver=0.1
    
    #TakeSS
    runAdbCommand(screenShot+".png")
    #Pull
    runAdbCommand(pull+".png")

    #ImageProcessing
    dist=matchTwoTemplates("screen.png")

    if dist>1000:
        factor=0.45


    print("Distance between is in pixels",dist)
    print("factor for distance is",factor)
    print("long press in ms is:",int(dist*factor))
    #Command based on distance
    pressScreen(int(dist*factor))
    # else:            
    #     print("Distance between is in pixels",dist)
    #     print("factor for distance is",factorOver)
    #     print("long press in ms is:",int(dist*factorOver))
    #     #Command based on distance
    #     pressScreen(int(dist*factorOver))

    print("waiting 15 secs")
    time.sleep(15)
    

    
