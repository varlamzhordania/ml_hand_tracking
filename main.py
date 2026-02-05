import cv2
import mediapipe as mp
import time
from modules.hand_detector import HandDetector
from modules.gesture_engine import GestureEngine
from controllers.basic import AppController

detector = HandDetector()
engine = GestureEngine()
controller = AppController()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )
    timestamp = int(time.time() * 1000)
    result = detector.find_hands(mp_image, timestamp)

    if result.hand_landmarks:
        for landmarks in result.hand_landmarks:
            finger_state = engine.get_fingers_up(landmarks)
            gesture = engine.identify(finger_state)
            controller.react(gesture)

            cv2.putText(
                frame,
                gesture,
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
