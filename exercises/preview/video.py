
import cv2
import time

def video_preview(video_cap, image, width, height):
    """ Aufruf des Videos und zeige Timer in the middle of the screen.
        Deklariere in File: video_cap = cv2.VideoCapture("path/to/video.mp4")
    """

    start_time = time.time()
    while video_cap.isOpened():
        success, frame = video_cap.read()
        
        if success:
            cv2.imshow("PythonGym", frame)

            elapsed_time = time.time() - start_time
            elapsed_time = int(round(elapsed_time, 2))
            cv2.putText(frame, str(elapsed_time), (int(width/2), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # if waitkey oder elapsed time > 3
            if cv2.waitKey(10) & 0xFF == ord('q') or elapsed_time > 3:
                video_cap.release()
                break
        
    cv2.imshow("PythonGym", image)
    video_cap.release()