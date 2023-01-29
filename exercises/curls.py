# PythomGym/exercises/curls.py
import cv2                              # OpenCV 
import mediapipe as mp                  # Mediapipe
import numpy as np                      # Numpy 
from angle import calculate_angle       # Winkelberechnung


# Funktion für Curl-Übung die in main.py aufgerufen wird
def curl(image, results, left_counter, right_counter):
            
    mp_pose = mp.solutions.pose

    


    # Zeigt Name der Übung an
    cv2.putText(image, 'Curls', (300,25), 
    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)


    # Erkennung erfolgreich 
    try:
        landmarks = results.pose_landmarks.landmark
        # Speichert Koordinaten für linke Seite
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        # berechnet Winkel für linke Seite
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        # Zeigt Winkel am linken Ellbogen an
        cv2.putText(image, str(round(left_angle,1)), 
                    tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # Speichert Koordinaten für rechte Seite
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        # berechnet Winkel für rechte Seite
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        # Zeigt Winkel am rechten Ellbogen an
        cv2.putText(image, str(round(right_angle,1)), 
                    tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # Zählt Curls wenn Winkel größer als 150 Grad und kleiner als 40 Grad ist und der Zustand "up" ist
        # linke Seite
        if left_angle > 150:
            left_stage = "up"
        if left_angle < 40  and left_stage == "up":
            left_stage = "down"
            left_counter +=1
        # rechte Seite
        if right_angle > 150:
            right_stage = "up"
        if right_angle < 40 and right_stage == "up":
            right_stage = "down"
            right_counter +=1
    # Erkennung nicht erfolgreich
    except:
        pass


     # Erkennung erfolgreich
    try:
        # Zeigt linien auf linke Seite
        cv2.line(image, tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), 
                tuple(np.multiply(left_elbow, [640, 480]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                tuple(np.multiply(left_wrist, [640, 480]).astype(int)), (255, 255, 255), 2)
        # Zeigt linien auf rechte Seite
        cv2.line(image, tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                tuple(np.multiply(right_elbow, [640, 480]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                tuple(np.multiply(right_wrist, [640, 480]).astype(int)), (255, 255, 255), 2)
        # Zeigt Anweisung auf linker Seite an 
        cv2.putText(image, str(left_stage), 
            tuple(np.multiply(left_elbow, [640, 550]).astype(int)), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA) 
        # Zeigt Anweisung auf rechter Seite an
        cv2.putText(image, str(right_stage), 
            tuple(np.multiply(right_elbow, [640, 550]).astype(int)), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Zeigt Counter für linke Seite an
        cv2.putText(image, str(left_counter),
            tuple(np.multiply(left_shoulder, [700, 450]).astype(int)), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # Zeigt Counter für rechte Seite an
        cv2.putText(image, str(right_counter),
            tuple(np.multiply(right_shoulder, [400, 450]).astype(int)), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # Erkennung nicht erfolgreich
    except:
        pass