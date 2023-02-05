import cv2
import mediapipe as mp
import numpy as np

# counter variables for pushups exercise
pushups_counter = 0
stage_pushups = None
invalid = False


def pushups(image, resultsPose, mp_pose, calculate_angle, width, height):
    global pushups_counter, stage_pushups, invalid

    # Zeigt Name mittig oben an
    cv2.putText(image, "Pushups", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(image, "Pushups", (int(width/2), 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    try:
        landmarks = resultsPose.pose_landmarks.landmark

        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        # logic for pushups exercise in elbow angle_elbow
        angle_elbow = calculate_angle(shoulder, elbow, wrist)
        angle_knee = calculate_angle(hip, knee, ankle)
        angle_hip = calculate_angle(shoulder, hip, knee)

        # logic for invalid pushups exercise, only use angle knee and hip for invalid
        if angle_knee < 170 or angle_hip < 170:
            invalid = True
        else:
            invalid = False


        # logic for pushups but not in the right position use the invalid variable
        if angle_elbow > 170 and invalid == False:
            stage_pushups = "down"
        if angle_elbow > 100 and invalid == False and stage_pushups == "down":
            stage_pushups = "up"
            pushups_counter += 1

    except:
        pass

    try:
        # draw lines for pushups exercise
        cv2.line(image, (shoulder[0], shoulder[1]), (elbow[0], elbow[1]), (0, 255, 0), 2)
        cv2.line(image, (elbow[0], elbow[1]), (wrist[0], wrist[1]), (0, 255, 0), 2)
        cv2.line(image, (hip[0], hip[1]), (knee[0], knee[1]), (0, 255, 0), 2)
        cv2.line(image, (knee[0], knee[1]), (ankle[0], ankle[1]), (0, 255, 0), 2)

        # draw circles for pushups exercise
        cv2.circle(image, (shoulder[0], shoulder[1]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(image, (elbow[0], elbow[1]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(image, (wrist[0], wrist[1]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(image, (hip[0], hip[1]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(image, (knee[0], knee[1]), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(image, (ankle[0], ankle[1]), 5, (0, 0, 255), cv2.FILLED)

        # draw pushups counter on shoulder
        cv2.putText(image, str(pushups_counter), (shoulder[0], shoulder[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, str(pushups_counter), (shoulder[0], shoulder[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        # draw invalid or valid on the left side
        if invalid == True:
            cv2.putText(image, "INVALID", (int(width/2)-200, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(image, "INVALID", (int(width/2)-200, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(image, "VALID", (int(width/2)-200, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(image, "VALID", (int(width/2)-200, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        
        # draw all angles on the body parts
        cv2.putText(image, str(int(angle_elbow)), (elbow[0], elbow[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(int(angle_knee)), (knee[0], knee[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(int(angle_hip)), (hip[0], hip[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        

        
    except:
        pass
