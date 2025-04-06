import cv2
import mediapipe as mp
import time
import subprocess
import os

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Button coordinates: (x, y, width, height)
exit_button = (100, 100, 200, 100)
 
 

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Draw "ESC" button
    cv2.rectangle(img, (exit_button[0], exit_button[1]),
                  (exit_button[0] + exit_button[2], exit_button[1] + exit_button[3]),
                  (246, 31, 139), cv2.FILLED)
    cv2.putText(img, "ESC", (exit_button[0] + 50, exit_button[1] + 65),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            h, w, c = img.shape
            lm = handLms.landmark[8]
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # Check button zones
            if exit_button[0] < cx < exit_button[0] + exit_button[2] and \
               exit_button[1] < cy < exit_button[1] + exit_button[3]:
                print("Exit button clicked!")
                cap.release()
                cv2.destroyAllWindows()
                exit()

          

    cv2.imshow("Hand Click Menu", img)
    cv2.moveWindow("Hand Click Menu", 0, 0)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
