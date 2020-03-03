import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import subprocess

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


def matchTwoTemplates(image,template1,template2):

    distance=0
    dists1=[]
    dists2=[]

    #Image read and transform
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    #Template read and transform
    templateM = cv2.imread(template1,0)
    w, h = templateM.shape[::-1]


    #Tempalte match
    res = cv2.matchTemplate(img_gray,templateM,cv2.TM_CCOEFF_NORMED)
    threshold = 0.65
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        #print(pt[0] + w, pt[1] + h)
        dists1.append(pt[1] + h)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)


    #Template read and transform
    templateS = cv2.imread(template2,0)
    w, h = templateS.shape[::-1]

        
    #Tempalte match
    res = cv2.matchTemplate(img_gray,templateS,cv2.TM_CCOEFF_NORMED)
    threshold = 0.87
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        #print(pt[0] + w, pt[1] + h)
        dists2.append(pt[1] + h)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite('res.png',img_rgb)
    #cv2.namedWindow('matched',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('matched', (600,600))
    #imageEdit=cv2.imread("res.png")
    #cv2.imshow("matched",imageEdit)

    print("dist of monster:",dists1[len(dists1)-1] )
    print("dist of pond:",dists2[len(dists2)-1] )
    print("dist of pond-2:",dists2[len(dists2)-1] )
    
    return dists2[len(dists2)-1]-dists1[len(dists1)-1]


while(True):

    #Factor for long press dists under 550
    factor=0.55
    #Factor for long press dists over 550
    factorOver=0.4
    
    #TakeSS
    runAdbCommand(screenShot+".png")
    #Pull
    runAdbCommand(pull+".png")

    #ImageProcessing
    dist=matchTwoTemplates("screen.png",templateMonster,pondBottom)

    if(dist<934):   
        print("Distance between is in pixels",dist)
        print("factor for distance is",factor)
        print("long press in ms is:",int(dist*factor))
        #Command based on distance
        pressScreen(int(dist*factor))
    else:            
        print("Distance between is in pixels",dist)
        print("factor for distance is",factorOver)
        print("long press in ms is:",int(dist*factorOver))
        #Command based on distance
        pressScreen(int(dist*factorOver))

    print("waiting 14 secs")
    time.sleep(14)
    

    
