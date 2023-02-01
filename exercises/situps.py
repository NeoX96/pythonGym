import cv2                              # OpenCV 
import mediapipe as mp                  # Mediapipe
import numpy as np                      # Numpy 
import time

# Lade das Video
cap = cv2.VideoCapture("exercises\pexels-rodnae-productions-8401327.mp4")


start_time = cv2.getTickCount()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    if elapsed_time > 3:
        break
    

    #Zeitanzeige 3 Sekunden 
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = ' {:.0f} sec'.format(elapsed_time)
    cv2.putText(frame, text, (frame.shape[1]//2, frame.shape[0]//2), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.imshow('Mediapipe Situp Feed', image)
time.sleep(3)



# Function for situp exercise that is called in main.py
def situp():

   
    # Initialize mediapipe modules
    mp_pose = mp.solutions.pose

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    

    # Counter variables for situp exercise
    situp_count = 0

  



    # Initialize mediapipe instance
    # min_detection_confidence: Minimum value for the probability in percent that a landmark was detected
    # min_tracking_confidence: Minimum value for the probability in percent that a landmark was detected
    with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
        while cap.isOpened():
            ret, frame = cap.read() 

            # Convert image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Flip image
            image = cv2.flip(image, 1)

            # Perform detection
            results = pose.process(image)

            # Convert image back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                shoulder_left = landmarks[5]
                shoulder_right = landmarks[6]
                hip_left = landmarks[11]
                hip_right = landmarks[12]
                

                # Berechne den Winkel zwischen Schultern und Hüfte
                angle = np.arctan2(shoulder_right.y - shoulder_left.y,
                                    shoulder_right.x - shoulder_left.x) - np.arctan2(hip_right.y - hip_left.y,
                                                                                    hip_right.x - hip_left.x)
                angle = angle * 180 / np.pi

                # Zeige den Rückenwinkel auf dem Bild an
                cv2.putText(image, "Rueckenwinkel: {:.2f}°".format(angle), (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



                    
                if angle > 100 and angle < 30 :
                    cv2.putText(image, 'SITUP', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
                    situp_count += 1
                    cv2.putText(image, "Correct", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(image, 'SITUP', (300,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
                    cv2.putText(image, "Incorrect", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            except:
                pass


            
            
            cv2.putText(image, "Count: {}".format(situp_count), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Mediapipe Situp Feed', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


# macht situp() ausführbar wenn nur dieses file ausgeführt wird
if __name__ == '__main__':
    situp()