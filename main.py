import time
import cv2 
import mediapipe as mp
from menu import menu
from exercises.curls import curl
from exercises.situps import situp
from angle import calculate_angle

state = 0
start_time = time.time()
currentFinger = 0
fingerCount = 0

# Video Capture
cap = cv2.VideoCapture(0)

# liest die Breite und Höhe der Kamera
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# setzt die Breite und Höhe der Kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# initialisiert Mediapipe Hands und Pose
with mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    with mp.solutions.pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
        
        # Starte Video Capture Loop
        while cap.isOpened():
            # success ist True, wenn ein Bild gelesen werden kann, frame enthält das Bild
            success, frame = cap.read()

            # success = False, wenn kein Bild gelesen werden kann
            if not success:
                cv2.putText(frame, "No image", (int(width/2), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
                break

            # Konvertiere Bild in RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # flip image
            image = cv2.flip(image, 1)
        
            # Führe Erkennung durch
            resultsPose = pose.process(image)
            resultsHands = hands.process(image)
        
            # Konvertiere Bild wieder in BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if currentFinger != fingerCount:
                currentFinger = fingerCount
                print("Finger count: ", fingerCount)

            # Zurücksetzen der Fingeranzahl, da Fingeranzahl ständig erhöht wird, wenn Finger erkannt werden
            fingerCount = 0
            

            if resultsHands.multi_hand_landmarks:
                
                for hand_landmarks in resultsHands.multi_hand_landmarks:
                    handLandmarks = []
                    # Get hand index to check label (left or right)
                    handIndex = resultsHands.multi_hand_landmarks.index(hand_landmarks)
                    handLabel = resultsHands.multi_handedness[handIndex].classification[0].label

                    # Fill list with x and y positions of each landmark
                    for landmarks in hand_landmarks.landmark:
                        handLandmarks.append([landmarks.x, landmarks.y])

                    # Test conditions for each finger: Count is increased if finger is 
                    #   considered raised.
                    # Thumb: TIP x position must be greater or lower than IP x position, 
                    #   deppeding on hand label.
                    if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                        fingerCount = fingerCount+1
                    elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                        fingerCount = fingerCount+1

                    # Other fingers: TIP y position must be lower than PIP y position, 
                    #   as image origin is in the upper left corner.
                    if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
                        fingerCount = fingerCount+1
                    if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
                        fingerCount = fingerCount+1
                    if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
                        fingerCount = fingerCount+1
                    if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
                        fingerCount = fingerCount+1

                    # Wenn state = 0 ist, wird das Hand Tracking angezeigt
                    if state == 0:
                        menu(image, hand_landmarks)
            
            # wenn 10 Finger oder 1 Finger erkannt werden, wird die Zeit gestoppt und angezeigt
            if currentFinger == 10 and state == 1 or currentFinger == 1 and state == 0:
                passedTime = time.time() - start_time

                # Zeit wird nur angezeigt, wenn sie kleiner als 3 Sekunden ist
                if passedTime < 3:
                    cv2.putText(image, str(round(passedTime, 1)), (int(width/2), 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

                # wenn 10 Finger erkannt werden, wird der state auf 1 gesetzt
                if time.time() - start_time > 3 and currentFinger == 10:
                    state = 0
                
                # wenn 1 Finger erkannt werden, wird der state auf 1 gesetzt
                if currentFinger == 1:
                    cv2.putText(image, "Curl", (50, int(height/2)+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Curl", (50, int(height/2)+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    if time.time() - start_time > 3:
                        state = 1

            # wenn keine Finger erkannt werden, wird die Zeit zurückgesetzt
            else:
                start_time = time.time()

            
            # Auruf der Übungen
            if state == 0:
                # Display finger count
                cv2.putText(image, str(fingerCount), (50, int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)


            # Aufruf der Curl-Übung
            if state == 1:
                curl(image, resultsPose, calculate_angle, width, height)
            
            # Aufruf der Situps-Übung
            if state == 2:
                situp(image, resultsPose, calculate_angle, width, height)

            # Aufruf der Squats-Übung
            if state == 3:
                pass
            
            

        # Display image
            cv2.imshow('MediaPipe Hands', image)
        # change windows size to camera resolution
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


