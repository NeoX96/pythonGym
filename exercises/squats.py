import cv2
import numpy as np
from .preview.video import video_preview

# counter variables for squat exercise
squats_counter = 0
stage_squats = None
video_cap = cv2.VideoCapture("exercises\preview\squats.mp4")
state_video_squat = False

def reset_squats():
    global squats_counter, stage_squats
    squats_counter = 0
    stage_squats = None

def squats(image, resultsPose, mp_pose, calculate_angle, width, height):
    """
        Übungslogik und Animation für Kniebeugen
    """

    if state_video_squat == False:
        video_preview(video_cap, image, width, height)



    # Zeigt Name mittig oben an
    cv2.putText(image, "Squats", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(image, "Squats", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if resultsPose.pose_landmarks:
        try:
            landmarks = resultsPose.pose_landmarks.landmark
            
            # wenn Ellbogen und Knie zu 50% sicher erkennbar sind
            if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5 and landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility > 0.5 and landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility > 0.5:

                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                angle_knee = calculate_angle(hip, knee, ankle)
                angle_hip = calculate_angle(shoulder, hip, knee)


                # logik für squats counter 
                global squats_counter, stage_squats

                if angle_hip > 170 and angle_knee > 170:
                    stage_squats = "down"
                if angle_hip < 85 and angle_knee < 70 and stage_squats == "down":
                    stage_squats = "up"
                    squats_counter += 1

                # wenn angle_hip kleiner als 120° und angle_knee größer als 160° dann ist die Übung nicht korrekt ausgeführt
                if angle_hip < 150 and angle_knee > 160:
                    color = (0,0,255)
                else:
                    color = (0,255,0)

                # Zeichne Counter
                cv2.putText(image, str(squats_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(image, str(squats_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)

                # Zeichne Kreise an den Winkel-Punkten die nicht filled sind
                cv2.circle(image, (int(shoulder[0]*width), int(shoulder[1]*height)), 10, color, cv2.FILLED)
                cv2.circle(image, (int(hip[0]*width), int(hip[1]*height)), 10, color, cv2.FILLED)
                cv2.circle(image, (int(knee[0]*width), int(knee[1]*height)), 10, color, cv2.FILLED)
                cv2.circle(image, (int(ankle[0]*width), int(ankle[1]*height)), 10, color, cv2.FILLED)

                # Zeichne Kreise an den Winkel-Punkten die filled sind
                cv2.circle(image, (int(shoulder[0]*width), int(shoulder[1]*height)), 15, color, 2)
                cv2.circle(image, (int(hip[0]*width), int(hip[1]*height)), 15, color, 2)
                cv2.circle(image, (int(knee[0]*width), int(knee[1]*height)), 15, color, 2)
                cv2.circle(image, (int(ankle[0]*width), int(ankle[1]*height)), 15, color, 2)

                # Zeichne Linien zwischen den Punkten
                cv2.line(image, (int(shoulder[0]*width), int(shoulder[1]*height)), (int(hip[0]*width), int(hip[1]*height)), color, 2)
                cv2.line(image, (int(hip[0]*width), int(hip[1]*height)), (int(knee[0]*width), int(knee[1]*height)), color, 2)
                cv2.line(image, (int(knee[0]*width), int(knee[1]*height)), (int(ankle[0]*width), int(ankle[1]*height)), color, 2)

                # Zeichne Winkel
                cv2.putText(image, str(int(angle_hip)), (int(hip[0]*width)-40, int(hip[1]*height)-50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                cv2.putText(image, str(int(angle_knee)), (int(knee[0]*width)-40, int(knee[1]*height)-50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

                # Zeichne Stage der Übung
                cv2.putText(image, stage_squats, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(image, stage_squats, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    
            else:
                cv2.putText(image, "Keine Person erkannt", (int(width/4), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
                cv2.putText(image, "Keine Person erkannt", (int(width/4), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        except:
            pass
