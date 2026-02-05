import cv2
import numpy as np


class AirCanvas:
    def __init__(self):
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.color = (255, 0, 255)  # Purple
        self.thickness = 5

    def draw(self, frame, mode, landmarks):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

        h, w, _ = frame.shape
        cx = int(landmarks[8].x * w)
        cy = int(landmarks[8].y * h)

        if mode == "DRAWING":
            if self.prev_x == 0 and self.prev_y == 0:
                self.prev_x, self.prev_y = cx, cy

            cv2.line(
                self.canvas,
                (self.prev_x, self.prev_y),
                (cx, cy),
                self.color,
                self.thickness
            )
            cv2.circle(frame, (cx, cy), 10, self.color, cv2.FILLED)

        elif mode == "SELECTION":
            cv2.circle(frame, (cx, cy), 15, (255, 255, 255), 2)
            self.prev_x, self.prev_y = 0, 0

        self.prev_x, self.prev_y = cx, cy

        frame_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv_mask = cv2.threshold(
            frame_gray,
            50,
            255,
            cv2.THRESH_BINARY_INV
        )
        inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)

        img_combined = cv2.bitwise_and(frame, inv_mask)
        img_combined = cv2.bitwise_or(img_combined, self.canvas)
        return img_combined
