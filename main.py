import time
import cv2 
import mediapipe as mp
from menu import menu
from exercises.curls import curl
from angle import calculate_angle

state = 1
start_time = time.time()

cap = cv2.VideoCapture(0)
currentFinger = 0
fingerCount = 0

# Zählvariablen für Curl-Übung
left_counter = 0 
right_counter = 0

left_stage = 0
right_stage = 0


with mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    with mp.solutions.pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
        
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                break

            # Konvertiere Bild in RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # flip image
            image = cv2.flip(image, 1)
        
            # Führe Erkennung durch
            resultsPose = pose.process(image)
            resultsHands = hands.process(image)
        
            # Konvertiere Bild wieder in BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if currentFinger != fingerCount:
                currentFinger = fingerCount
                print("Finger count: ", fingerCount)

            # Reset finger count
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
            if currentFinger == 10 or currentFinger == 1:
                passedTime = time.time() - start_time

                # Zeit wird nur angezeigt, wenn sie kleiner als 3 Sekunden ist
                if passedTime < 3:
                    cv2.putText(image, str(round(passedTime, 1)), (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

                # wenn 10 Finger erkannt werden, wird der state auf 1 gesetzt
                if time.time() - start_time > 3 and currentFinger == 10:
                    state = 0
                
                # wenn 1 Finger erkannt werden, wird der state auf 1 gesetzt
                if time.time() - start_time > 3 and currentFinger == 1:
                    state = 1

            # wenn keine Finger erkannt werden, wird die Zeit zurückgesetzt
            else:
                start_time = time.time()

            
            # Auruf der Übungen
            if state == 0:
                # Display finger count
                cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
            
            # Aufruf der Curl-Übung
            if state == 1:
                curl(image, resultsPose, left_counter, right_counter, calculate_angle, left_stage, right_stage)
            
            # Aufruf der Situps-Übung
            if state == 2:
                pass

            # Aufruf der Squats-Übung
            if state == 3:
                pass
            
            

        # Display image
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


