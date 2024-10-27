import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = pTime = 0

detector = htm.handDetector(maxHands= 1,detectionCon = 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange() #(-96.0, 0.0, 0.125)

minVol = volRange[0] #-96
maxVol = volRange[1] #0
minlength_c = 25 #25
maxlength_c = 175 #175
estimated_distance_c = 37.5

vol = 0
volBar = 400
volPer = 0

known_distance = 30  # Distance in cm when the hand size is known_size
known_size = 300  # The size of the hand in pixels at known_distance

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if not(success):
        print("Hand not read")

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        x3, y3 = lmList[0][1], lmList[0][2]
        x4, y4 = lmList[12][1], lmList[12][2]
        pixel_length_hand = math.hypot(x4 - x3, y4 - y3)

        estimated_distance = (known_size * known_distance) / pixel_length_hand

        minlength = (minlength_c*estimated_distance_c) / estimated_distance
        maxlength = (maxlength_c*estimated_distance_c) / estimated_distance

        length = math.hypot(x2-x1,y2-y1)

        vol = np.interp(length, [minlength, maxlength], [minVol, maxVol])
        volBar = np.interp(length, [minlength, maxlength], [400,150])
        volPer = np.interp(length, [minlength, maxlength], [0,100])
        dB = 34 * math.log((volPer) / 100, 10) if volPer>0 else minVol
        if minVol <= dB <= maxVol:
            volume.SetMasterVolumeLevel(dB, None)

        cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        if volPer < 1 or volPer > 99:
            cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
    
    cv2.rectangle(img, (50,150), (85,400), (0, 255, 0), 3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img,f"{int(volPer)} %",(40,450), cv2.FONT_HERSHEY_COMPLEX, 1, 
                (255, 0, 0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,f"FPS: {int(fps)}",(40,50), cv2.FONT_HERSHEY_COMPLEX, 1, 
                (255, 0, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()