import cv2                              # OpenCV 
import numpy as np                      # Numpy 


#Lade das Video
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



# Zählvariablen für Situps
left_counter_situps = 0 
right_counter_situps = 0
stage_situps = None

#Zähler variable
situp_count = 0

def reset_situps():
    global left_counter_situps, right_counter_situps, stage_situps, situp_count
    left_counter_situps = 0 
    right_counter_situps = 0
    stage_situps = None
    situp_count = 0

#. Funktion für Curl-Übung die in main.py aufgerufen wird
def situp(image, resultsPose, mp_pose, calculate_angle, width, height):

    global stage_situps, left_counter_situps, right_counter_situps, situp_count


    #. Zeigt Name der Übung an
    cv2.putText(image, 'Situps', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
    cv2.putText(image, 'Situps', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    
 
    #. Erkennung war erfolgreich

    try:
        landmarks = resultsPose.pose_landmarks.landmark

        
        #. Speichert Koordinaten für linke Seite
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        #. Speichert Koordinaten für rechte Seite
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        
        #. Berechne den Winkel linke Seite
        left_angle_situps = calculate_angle(left_shoulder, left_hip, left_knee)

        #. Berechne den Winkel rechte Seite
        right_angle_situps = calculate_angle(right_shoulder, right_hip, right_knee)



    
        #. Zeigt Winkel für Sit-Ups am linken Knie an
        cv2.putText(image, str(round(left_angle_situps,1)), 
                    tuple(np.multiply(left_knee, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, str(round(left_angle_situps,1)), 
                    tuple(np.multiply(left_knee, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


        #. Zeigt Winkel für Sit-Ups am rechten Knie an
        cv2.putText(image, str(round(right_angle_situps,1)), 
                    tuple(np.multiply(right_knee, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, str(round(right_angle_situps,1)), 
                    tuple(np.multiply(right_knee, [width, height]).astype(int)), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


        
        # logik für Linke seite
        if left_angle_situps > 100:
            stage_situps = "up"
        if left_angle_situps < 40  and stage_situps == "up":
            stage_situps = "down"
            
            situp_count += 1

            
            left_bar_height1 = int(height * (1 - right_angle / 200))
            

     
    

        # logik für rechte Seite
        if right_angle_situps > 100:
            stage_situps = "up"
        if right_angle_situps < 30  and stage_situps == "up":
            stage_situps = "down"
         
            situp_count += 1
      
      
            right_bar_height1 = int(height * (1 - left_angle / 200))
      

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