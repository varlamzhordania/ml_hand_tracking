import math


class GestureEngine:
    @staticmethod
    def get_distance(p1, p2):
        """Calculates the Euclidean distance between two landmarks."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def get_fingers_up(self, landmarks):
        """
        Returns a list of 5 integers (1 for up, 0 for down) using
        """
        fingers = []

        thumb_dist = self.get_distance(landmarks[4], landmarks[17])
        thumb_threshold = self.get_distance(landmarks[2], landmarks[17])

        if thumb_dist > thumb_threshold:
            fingers.append(1)
        else:
            fingers.append(0)

        tips = [8, 12, 16, 20]
        knuckles = [5, 9, 13, 17]
        wrist = landmarks[0]

        for tip, knuckle in zip(tips, knuckles):
            dist_tip = self.get_distance(landmarks[tip], wrist)
            dist_knuckle = self.get_distance(landmarks[knuckle], wrist)

            if dist_tip > dist_knuckle:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def identify(self, fingers):
        if fingers == [1, 1, 1, 1, 1]: return "Open Palm"
        if fingers == [0, 0, 0, 0, 0]: return "Fist"
        if fingers == [0, 1, 0, 0, 0]: return "Pointer"
        if fingers == [1, 0, 0, 0, 0]: return "Like"
        if fingers == [0, 1, 1, 0, 0]: return "Peace"
        return "Unknown"

    def get_drawing_mode(self, fingers):
        if fingers == [0, 1, 0, 0, 0]:
            return "DRAWING"
        elif fingers == [0, 1, 1, 0, 0]:
            return "SELECTION"
        return "IDLE"

    def get_system_gesture(self, landmarks):
        thumb_tip = landmarks[4]
        index_knuckle = landmarks[5]

        if thumb_tip.y < index_knuckle.y - 0.05:
            return "THUMBS_UP"
        elif thumb_tip.y > index_knuckle.y + 0.05:
            return "THUMBS_DOWN"
        return None