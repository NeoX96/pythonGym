import cv2                              # OpenCV 
import mediapipe as mp                  # Mediapipe
import numpy as np                      # Numpy 

# Lade das Video
# cap = cv2.VideoCapture("exercises\pexels-rodnae-productions-8401327.mp4")
# 
# 
# start_time = cv2.getTickCount()
# 
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
# 
#     elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
#     if elapsed_time > 3:
#         break
#     
# 
#     #Zeitanzeige 3 Sekunden 
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     text = ' {:.0f} sec'.format(elapsed_time)
#     cv2.putText(frame, text, (frame.shape[1]//2, frame.shape[0]//2), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
#     
#     cv2.imshow("Video", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# 
# 
# cv2.imshow('Mediapipe Situp Feed', image)
# time.sleep(3)

# Zählvariablen für Curl-Übung
left_counter_situps = 0 
right_counter_situps = 0
stage_situps = None

# Counter variables for situp exercise
situp_count = 0

# Function for situp exercise that is called in main.py
def situp(image, resultsPose, calculate_angle, width, height):

    global stage_situps, left_counter_situps, right_counter_situps, situp_count

    # Mediapipe Pose
    mp_pose = mp.solutions.pose

    # Zeigt Name der Übung an
    cv2.putText(image, 'Situps', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
    cv2.putText(image, 'Situps', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    


    try:
        landmarks = resultsPose.pose_landmarks.landmark

        
        # Speichert Koordinaten für linke Seite
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        # Speichert Koordinaten für rechte Seite
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        
        # Berechne den Winkel linke Seite
        left_angle_situps = calculate_angle(left_shoulder, left_hip, left_knee)

        # Berechne den Winkel rechte Seite
        right_angle_situps = calculate_angle(right_shoulder, right_hip, right_knee)


        # logik für Linke seite
        if left_angle_situps > 175:
            stage_situps = "up"
        if left_angle_situps < 115  and stage_situps == "up":
            stage_situps = "down"
            situp_count += 1

        # logik für rechte Seite
        #
        #
        #
        #

            
        # wenn Winkel über 100 und unter 30 ist, dann ist die Übung korrekt, ansonsten falsch
        if left_angle_situps > 100 and left_angle_situps < 30 :
            cv2.putText(image, "Correct", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Incorrect", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    except:
        pass
    

    try: 
        # Zeichnet die Wiederholungen
        cv2.putText(image, "Count: " + str(situp_count), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Zeichnet die Stages
        cv2.putText(image, "Stage: " + str(stage_situps), (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Zeichnet die Winkel für linke Seite
        cv2.putText(image, str(left_angle_situps),
            tuple(np.multiply(left_hip, [width+100, height-70]).astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        

        # Zeichnet lininen für linke Seite 
        cv2.line(image, tuple(np.multiply(left_shoulder, [width, height]).astype(int)),
            tuple(np.multiply(left_hip, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(left_knee, [width, height]).astype(int)),
            tuple(np.multiply(left_hip, [width, height]).astype(int)), (255, 255, 255), 2)
        
        # Zeichnet roten punkt auf hip für linke Seite
        cv2.circle(image, tuple(np.multiply(left_hip, [width, height]).astype(int)), 5, (0, 0, 255), -1)


    except:
        pass