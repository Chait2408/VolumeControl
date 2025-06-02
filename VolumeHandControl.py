import cv2
import time
import numpy as np
import HandTrackingModule as htm 
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


###
wCam, hCam = 640, 480  # Width and height of the camera feed
###

cap = cv2.VideoCapture(0)  # Use 0 for the default camera
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height
pTime = 0  # Previous time for FPS calculation

detector = htm.HandDetector(detectionCon=0.7)  # Initialize hand detector

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()

    img = detector.findHands(img)  # Detect hands in the image
    lmList = detector.findPosition(img, draw=False)  # Get the positions of landmarks
    if len(lmList) != 0:
        # print(lmList[8], lmList[4])  # Print the coordinates of the index finger tip(8) and thumb tip(4)

        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip coordinates
        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger tip coordinates
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # Draw circle on thumb tip
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)  # Draw circle on index finger tip
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)         # Draw line between thumb and index finger tips
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)    # Draw circle at the midpoint between thumb and index finger tips

        length = math.hypot(x2 - x1, y2 - y1)  # Calculate the distance between thumb and index finger tips
        print(length)

        # hand range 50 - 300
        # volume range -65 - 0

        vol = np.interp(length, [50, 300], [minVol, maxVol])  # Map the length to volume range
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)  # Set the system volume

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)  # Draw volume bar rectangle
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)  # Draw volume bar
    cv2.putText(img, f'Volume: {int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # Display volume level


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break
cap.release()
cv2.destroyAllWindows()