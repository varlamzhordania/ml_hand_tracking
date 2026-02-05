class GestureEngine:
    @staticmethod
    def get_fingers_up(landmarks):
        """Returns a list of 5 integers (1 for up, 0 for down)"""
        fingers = []
        if landmarks[4].x > landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        tips = [8, 12, 16, 20]
        for tip in tips:
            if landmarks[tip].y < landmarks[tip - 2].y:
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
        if landmarks[4].y < landmarks[3].y and landmarks[4].y < landmarks[
            8].y:
            return "THUMBS_UP"
        elif landmarks[4].y > landmarks[3].y and landmarks[4].y > \
                landmarks[8].y:
            return "THUMBS_DOWN"
        return None

