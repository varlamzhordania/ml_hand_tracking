import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'tasks/hand_landmarker.task'

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)

detector = HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

    result = detector.detect_for_video(mp_image, timestamp_ms)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            tips = [8, 12, 16, 20]
            fingers_up = []

            for tip in tips:
                if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

            if hand_landmarks[4].x > hand_landmarks[3].x:
                fingers_up.insert(0, 1)
            else:
                fingers_up.insert(0, 0)

            total_fingers = fingers_up.count(1)

            gesture_text = "None"
            if total_fingers == 5:
                gesture_text = "Open Palm"
            elif fingers_up == [0, 1, 1, 0, 0]:
                gesture_text = "Peace Sign"
            elif fingers_up == [0, 1, 0, 0, 0]:
                gesture_text = "Pointing"
            elif total_fingers == 0:
                gesture_text = "Fist"

            cv2.putText(
                frame, f"Gesture: {gesture_text}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
            )

    cv2.imshow('Modern Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

detector.close()
cap.release()
cv2.destroyAllWindows()
