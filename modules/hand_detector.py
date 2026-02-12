from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:
    def __init__(self, model_path='tasks/hand_landmarker.task'):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence = 0.5,
            min_hand_presence_confidence = 0.5,
            min_tracking_confidence = 0.6
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def find_hands(self, mp_image, timestamp):
        return self.detector.detect_for_video(mp_image, timestamp)


class LandmarkSmoother:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.previous_values = {}

    def smooth(self, landmark_id, current_x, current_y):
        if landmark_id not in self.previous_values:
            self.previous_values[landmark_id] = (current_x, current_y)
            return current_x, current_y

        prev_x, prev_y = self.previous_values[landmark_id]

        smoothed_x = (self.alpha * current_x) + (1 - self.alpha) * prev_x
        smoothed_y = (self.alpha * current_y) + (1 - self.alpha) * prev_y

        self.previous_values[landmark_id] = (smoothed_x, smoothed_y)

        return smoothed_x, smoothed_y