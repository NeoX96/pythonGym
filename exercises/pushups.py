import cv2
import numpy as np

# counter variables for pushups exercise
pushups_counter = 0
stage_pushups = None
invalid = False

def reset_pushups():
    global pushups_counter, stage_pushups, invalid
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
        # zeichne linien für pushups exercise
        cv2.line(image, tuple(np.multiply(shoulder, [width, height]).astype(int)), 
                tuple(np.multiply(elbow, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(elbow, [width, height]).astype(int)),
                tuple(np.multiply(wrist, [width, height]).astype(int)), (255, 255, 255), 2)
        
        cv2.line(image, tuple(np.multiply(hip, [width, height]).astype(int)),
                tuple(np.multiply(knee, [width, height]).astype(int)), (255, 255, 255), 2)
        cv2.line(image, tuple(np.multiply(knee, [width, height]).astype(int)),
                tuple(np.multiply(ankle, [width, height]).astype(int)), (255, 255, 255), 2)
        
        # zeichne Kreise für pushups exercise
        cv2.circle(image, tuple(np.multiply(shoulder, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(elbow, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(wrist, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        
        cv2.circle(image, tuple(np.multiply(hip, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(knee, [width, height]).astype(int)), 5, (0, 0, 255), -1)
        cv2.circle(image, tuple(np.multiply(ankle, [width, height]).astype(int)), 5, (0, 0, 255), -1)

        # zeichne Kreise für pushups exercise
        cv2.putText(image, str(int(angle_elbow)), tuple(np.multiply(elbow, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(int(angle_knee)), tuple(np.multiply(knee, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(int(angle_hip)), tuple(np.multiply(hip, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Pushups Counter Text
        cv2.putText(image, str(pushups_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(pushups_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1, cv2.LINE_AA)



        
    except:
        pass
