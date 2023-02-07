import time
import cv2 
import mediapipe as mp
from menu import menu
from exercises.curls import curl, reset_curls
from exercises.situps import situp, reset_situps
from exercises.squats import squats, reset_squats
from exercises.pushups import pushups, reset_pushups
from angle import calculate_angle

state = 2
start_time = time.time()
currentFinger = 0
fingerCount = 0
combined_image = None


# Video Capture
cap = cv2.VideoCapture(0)
overlay = cv2.imread("exercises\preview\steuerung.png")


# liest die Breite und Höhe der Kamera
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

desired_width = int(height * 16 / 9)
if desired_width > width:
    width = desired_width
    height = int(width * 9 / 16)
else:
    height = int(width * 9 / 16)
    width = desired_width

# setzt die Breite und Höhe der Kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# öffnet das Fenster in Vollbild und maximiert es
cv2.namedWindow("PythonGym", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("PythonGym", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# initialisiert Mediapipe Hands und Pose
with mp.solutions.hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, model_complexity=1) as hands:
    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False, smooth_landmarks=True, model_complexity=1, enable_segmentation=False) as pose:
        
        # Starte Video Capture Loop
        while cap.isOpened():

            # success ist True, wenn ein Bild gelesen werden kann, frame enthält das Bild
            success, frame = cap.read()

            # success = False, wenn kein Bild gelesen werden kann
            if not success:
                cv2.putText(frame, "No image", (int(width/2), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
                break

            # Skaliere das Frame auf eine bestimmte Größe
            frame = cv2.resize(frame, (width, height))
            
            # Konvertiere Bild in RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # flip image
            image = cv2.flip(image, 1)
        
            # Führe Erkennung durch
            resultsPose = pose.process(image)
            resultsHands = hands.process(image)
        
            # Konvertiere Bild wieder in BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_pose = mp.solutions.pose

            # dadruch das fingerCount immer aktualisiert wird, kann man darauf nicht vergleichend
            # deshalb currentFinger, die nur aktualisiert wird, wenn sich die Fingeranzahl ändert
            if currentFinger != fingerCount:
                currentFinger = fingerCount
                print("Finger count: ", fingerCount)

            # Zurücksetzen der Fingeranzahl, da Fingeranzahl ständig erhöht wird, wenn Finger erkannt werden
            fingerCount = 0

            # wenn Hand erkannt wird, werden die Finger gezählt
            if resultsHands.multi_hand_landmarks:
                # Für jede Hand werden die Landmarks ausgelesen	
                for hand_landmarks in resultsHands.multi_hand_landmarks:
                    handLandmarks = []
                    handIndex = resultsHands.multi_hand_landmarks.index(hand_landmarks)
                    handLabel = resultsHands.multi_handedness[handIndex].classification[0].label

                    # Für jeden Landmark wird der x und y Wert ausgelesen
                    for landmarks in hand_landmarks.landmark:
                        handLandmarks.append([landmarks.x, landmarks.y])

                    # If abfrage für jeden Finger: Zähler wird erhöht, wenn Finger gehoben wird 
                    # Thumb: TIP x position must be greater or lower than IP x position, 
                    #   deppeding on hand label.
                    if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                        fingerCount = fingerCount+1
                    elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                        fingerCount = fingerCount+1

                    # Other fingers: TIP y position must be lower than PIP y position, 
                    #   as image origin is in the upper left corner.
                    if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
                        fingerCount = fingerCount+1
                    if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
                        fingerCount = fingerCount+1
                    if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
                        fingerCount = fingerCount+1
                    if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
                        fingerCount = fingerCount+1

                    # Wenn state = 0 ist, wird das Hand Tracking angezeigt
                    if state == 0:
                        menu(image, hand_landmarks)
            
            # vergangene Zeit wird berechnet
            passedTime = time.time() - start_time

            # 10 Finger (wenn in Übung kann zurück zum Hauptmenü gewechselt werden oder im Hauptmenü kann Anwendung beendet werden)
            # oder 1-4 Finger und State = 0 (wenn im Hauptmenü kann Übung gewählt werden)
            # oder 5 Finger und State größer 0 (wenn in Übung kann Reset gewählt werden)
            if (currentFinger == 10) or (1 <= currentFinger <= 4 and state == 0) or (currentFinger == 5 and state > 0):

                # wenn sich finger ändern, wird die Zeit zurückgesetzt
                if currentFinger != fingerCount:
                    start_time = time.time()
                    passedTime = 0

                # Animation er Zeit (3 Sekunden Zeit zum Auswählen)
                if passedTime < 3:
                    # Breite des Balkens
                    bar_width = int(width/3)

                    # Koordinaten für linke und rechte Seite des Balkens
                    x1 = int(width/2 - bar_width/2)
                    x2 = int(width/2 + bar_width/2)

                    # Y-Koordinate für die obere Kante des Balkens
                    bar_y = height - 30

                    # Vollständigen Balken zeichnen (weiße Farbe)
                    cv2.rectangle(image, (x1, bar_y), (x2, height), (255, 255, 255), -1)

                    # Zeichne einen Kreis, um die eckige Form des Balkens zu verdecken (türkis Farbe)
                    # Balken zeichnen, der die verstrichene Zeit darstellt (türkis Farbe)
                    #cv2.circle(image, (x1 + int(bar_width*(passedTime/3)), bar_y + 10), 10, (255, 255, 0), -1)
                    cv2.rectangle(image, (x1, bar_y), (x1 + int(bar_width*(passedTime/2)), height), (255, 255, 0), -1)

                    # set timer text in the middle of the bar 3 - passed time
                    cv2.putText(image, str(int(3.5 - passedTime)), (int(width/2), bar_y + 19), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, str(int(3.5 - passedTime)), (int(width/2), bar_y + 19), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

                    # schwarze Balken 
                    cv2.rectangle(image, (width - bar_width, height - 30), (width, height), (0, 0, 0), -1)
                    cv2.rectangle(image, (width - bar_width*4, height - 30), (width - bar_width*2, height), (0, 0, 0), -1)

                # wenn Zeit größer als 3 Sekunden ist und 10 Finger erkannt werden, wird der state auf 0 gesetzt
                if currentFinger == 10:
                    if state > 0:
                        cv2.putText(image, "Back", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)
                        cv2.putText(image, "Back", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                        if passedTime > 3:
                            state = 0
                            passedTime = 0
                            start_time = time.time()
                    if state == 0:
                        cv2.putText(image, "Exit", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                        cv2.putText(image, "Exit", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)
                        if passedTime > 3:
                            cap.release()
                            cv2.destroyAllWindows()
                            break

                # wenn in Übung - 5 Finger erkannt werden, wird Reset angezeigt und nach 3 Sekunden Variablen zurückgesetzt
                if currentFinger == 5:
                    cv2.putText(image, "Reset", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Reset", (100, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    
                    if passedTime > 3:
                        if state == 1:
                            reset_curls()

                        if state == 2:
                            reset_situps()

                        if state == 3:
                            reset_squats()
                        
                        if state == 4:
                            reset_pushups()

                # wenn 1 Finger erkannt wird und state = 0 ist
                if currentFinger == 1 and state == 0:
                    cv2.putText(image, "Curl starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Curl starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    if passedTime > 3:
                        state = 1

                # wenn 2 Finger erkannt werden und state = 0 ist
                if currentFinger == 2 and state == 0:
                    cv2.putText(image, "Situps starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Situps starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    if passedTime > 3:
                        state = 2

                # wenn 3 Finger erkannt werden und state = 0 ist
                if currentFinger == 3 and state == 0:
                    cv2.putText(image, "Squats starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Squats starten in", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    if passedTime > 3:
                        state = 3
                
                # wenn 4 Finger erkannt werden und state = 0 ist
                if currentFinger == 4 and state == 0:
                    cv2.putText(image, "Pushups starten in ", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 4, cv2.LINE_AA)
                    cv2.putText(image, "Pushups starten in ", (10, int(height)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    if passedTime > 3:
                        state = 4

            # wenn keine Finger erkannt werden, wird die Zeit zurückgesetzt
            else:
                start_time = time.time()

            
            # Auruf der Übungen
            if state == 0:
                # Display finger count
                cv2.putText(image, str(fingerCount), (50, int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

            # Aufruf der Curl-Übung
            if state == 1:
                curl(image, resultsPose, mp_pose, calculate_angle, width, height)
                pass
            
            # Aufruf der Situps-Übung
            if state == 2:
                situp(image, resultsPose, mp_pose, calculate_angle, width, height)
                pass

            # Aufruf der Squats-Übung
            if state == 3:
                squats(image, resultsPose, mp_pose, calculate_angle, width, height)
                pass
            
            # Aufruf der Pushups-Übung
            if state == 4:
                pushups(image, resultsPose, mp_pose, calculate_angle, width, height)
                pass
            
            # imshow
            if state == 0:
                overlay = cv2.resize(overlay, (width, height))
                combined_image = cv2.addWeighted(image, 0.2, overlay, 1, 0)
                if combined_image is not None:
                    cv2.imshow('PythonGym', combined_image)
            else:
                cv2.imshow('PythonGym', image)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break


