import cv2
import numpy as np
from .preview.video import video_preview

# Zählvariablen für Pushups
pushup_counter = 0
stage_pushup = None

# auslesen des Videos
video_cap = cv2.VideoCapture("exercises\preview\pushups.mp4")
state_video_pushup = False

# Zustand für Pushups zurückzusetzen
def reset_pushups():
    global pushup_counter, stage_pushup
    pushup_counter = 0
    stage_pushup = None


# Funktion für die Liegestützübung die in der main.py aufgerufen wird
def pushups(image, resultsPose, mp_pose, calculate_angle, width, height):
    """ 
        Übungslogik und Animation für Liegestützen
    """

    # Zeige Video an
    global state_video_pushup

    if state_video_pushup == False:
        video_preview(video_cap, image, width, height)




    global pushup_counter, stage_pushup
    
    #. Zeigt Name der Übung an
    cv2.putText(image, "Pushups", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(image, "Pushups", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)


    try:
        landmarks = resultsPose.pose_landmarks.landmark

         # Definiert die Koordinaten(x,y) von Ellenbogen, Schulter, Hüfte,Handgelenk und Knie 
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

         # brechnet die Winkel zwischen drei Punkten (Handgelenk, Ellbogen,Schulter) (ellbogen, Schulter, Hüfte) und (Schülter, Hüfte, Knie)
        elbow_angle = calculate_angle(wrist, elbow, shoulder)
        shoulder_angle = calculate_angle(elbow, shoulder, hip)
        hip_angle = calculate_angle(shoulder, hip, knee)

        # Logik für Pushups
        if elbow_angle > 160 and hip_angle > 140 and hip_angle < 190:
                stage_pushup = "down"
        if elbow_angle < 120 and stage_pushup == "down" and hip_angle > 140 and hip_angle <190:
            stage_pushup = "up"
            pushup_counter += 1   
                 
    except:
        pass

    try: 
        # Linie zwischen Schulter und Ellenbogen
        cv2.line(image, tuple(np.multiply(shoulder, [width, height]).astype(int)), 
                tuple(np.multiply(elbow, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(elbow, [width, height]).astype(int)),
                tuple(np.multiply(wrist, [width, height]).astype(int)), (255, 255, 255), 2)
        
        # Linie zwischen Schulter und Hüfte
        cv2.line(image, tuple(np.multiply(shoulder, [width, height]).astype(int)),
                tuple(np.multiply(hip, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(hip, [width, height]).astype(int)),
                tuple(np.multiply(knee, [width, height]).astype(int)), (255, 255, 255), 2)
        
        cv2.circle(image, tuple(np.multiply(elbow, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(shoulder, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(hip, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(wrist, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(knee, [width, height]).astype(int)), 5, (0, 0, 255), -1)

        # Zeigt Winkel an
        cv2.putText(image, str(int(elbow_angle)), tuple(np.multiply(elbow, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(int(shoulder_angle)), tuple(np.multiply(shoulder, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(int(hip_angle)), tuple(np.multiply(hip, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        

       # Zeigt Anzahl der Pushups an
        cv2.putText(image, str(pushup_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
        cv2.putText(image, str(pushup_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Zeigt Richtung an
        cv2.putText(image, stage_pushup, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, stage_pushup, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)


        



    except:
        pass

