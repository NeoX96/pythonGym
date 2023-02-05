# PythomGym/exercises/curls.py
import cv2                              # OpenCV 
import numpy as np                      # Numpy 


# Zählvariablen für Curl-Übung
left_counter_curls = 0 
right_counter_curls = 0

left_stage_curls = None
right_stage_curls = None

# Zurücksetzen der Zählvariablen für Curl-Übung
def reset_curls():
    global left_counter_curls, right_counter_curls, left_stage_curls, right_stage_curls
    
    left_counter_curls = 0 
    right_counter_curls = 0
    left_stage_curls = None
    right_stage_curls = None


# Funktion für Curl-Übung die in main.py aufgerufen wird
def curl(image, results, mp_pose, calculate_angle, width, height):
    
    global left_counter_curls, right_counter_curls, left_stage_curls, right_stage_curls


    # Zeigt Name der Übung an
    cv2.putText(image, 'Curls', (300,25), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
    cv2.putText(image, 'Curls', (300,25), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)


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
                    tuple(np.multiply(left_elbow, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, str(round(left_angle,1)), 
                    tuple(np.multiply(left_elbow, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Speichert Koordinaten für rechte Seite
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # berechnet Winkel für rechte Seite
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Zeigt Winkel am rechten Ellbogen an
        cv2.putText(image, str(round(right_angle,1)), 
                    tuple(np.multiply(right_elbow, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, str(round(right_angle,1)), 
                    tuple(np.multiply(right_elbow, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Zählt Curls wenn Winkel größer als 150 Grad und kleiner als 40 Grad ist und der Zustand "up" ist
        # linke Seite
        if left_angle > 140:
            left_stage_curls = "up"
        if left_angle < 50  and left_stage_curls == "up":
            left_stage_curls = "down"
            left_counter_curls +=1

        # rechte Seite
        if right_angle > 150:
            right_stage_curls = "up"
        if right_angle < 40 and right_stage_curls == "up":
            right_stage_curls = "down"
            right_counter_curls +=1

        right_bar_height = int(height * (1 - left_angle / 200))
        left_bar_height = int(height * (1 - right_angle / 200))

    # Erkennung nicht erfolgreich
    except:
        pass


    # Erkennung erfolgreich
    try:
        # Zeigt linien auf linke Seite
        cv2.line(image, tuple(np.multiply(left_shoulder, [width, height]).astype(int)), 
                tuple(np.multiply(left_elbow, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(left_elbow, [width, height]).astype(int)),
                tuple(np.multiply(left_wrist, [width, height]).astype(int)), (255, 255, 255), 2)

        # Zeigt linien auf rechte Seite
        cv2.line(image, tuple(np.multiply(right_shoulder, [width, height]).astype(int)),
            tuple(np.multiply(right_elbow, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(right_elbow, [width, height]).astype(int)),
            tuple(np.multiply(right_wrist, [width, height]).astype(int)), (255, 255, 255), 2)


        # Zeigt Anweisung auf linker Seite an 
        cv2.putText(image, str(left_stage_curls),
            tuple(np.multiply(left_elbow, [width-100, height+80]).astype(int)),
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(image, str(left_stage_curls), 
            tuple(np.multiply(left_elbow, [width-100, height+80]).astype(int)), 
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 1, cv2.LINE_AA) 


        # Zeigt Anweisung auf rechter Seite an
        cv2.putText(image, str(right_stage_curls),
            tuple(np.multiply(right_elbow, [width-100, height+80]).astype(int)),
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(image, str(right_stage_curls), 
            tuple(np.multiply(right_elbow, [width-100, height+80]).astype(int)), 
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 1, cv2.LINE_AA)

                
        # Zeigt Counter für linke Seite an
        cv2.putText(image, str(left_counter_curls),
            tuple(np.multiply(left_shoulder, [width+100, height-70]).astype(int)),
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(image, str(left_counter_curls),
            tuple(np.multiply(left_shoulder, [width+100, height-70]).astype(int)), 
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,255), 2, cv2.LINE_AA)
        
        
        # Zeigt Counter für rechte Seite an
        cv2.putText(image, str(right_counter_curls),
            tuple(np.multiply(right_shoulder, [width-250, height-70]).astype(int)),
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(image, str(right_counter_curls),
            tuple(np.multiply(right_shoulder, [width-250, height-70]).astype(int)), 
            cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,255), 2, cv2.LINE_AA)
        
        # zeichnet kreise um Ellbogen
        cv2.circle(image, tuple(np.multiply(left_elbow, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(left_elbow, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_elbow, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_elbow, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)

        # zeichnet kreise um Schulter
        cv2.circle(image, tuple(np.multiply(left_shoulder, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(left_shoulder, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_shoulder, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_shoulder, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)

        # zeichnet kreise um Handgelenk
        cv2.circle(image, tuple(np.multiply(left_wrist, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(left_wrist, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_wrist, [width, height]).astype(int)), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, tuple(np.multiply(right_wrist, [width, height]).astype(int)), 5, (255, 255, 255), 2, cv2.LINE_AA)

        # Balken für linke Seite
        cv2.rectangle(image, (25, height-left_bar_height), (75, height), (0,255,0), -1)

        # Balken für rechte Seite
        cv2.rectangle(image, (width-75, height-right_bar_height), (width-25, height), (0, 255, 0), -1)



    # Erkennung nicht erfolgreich
    except:
        pass