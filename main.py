import customtkinter as ctk
import cv2
import mediapipe as mp
import pyautogui
import time
import math
from PIL import Image

from controllers.aircanvas import AirCanvas
from modules.hand_detector import HandDetector
from modules.gesture_engine import GestureEngine

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
pyautogui.FAILSAFE = True


class VisionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hand Vision")
        self.geometry("1200x700")

        # --- Sidebar UI ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="Select Mode",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=20)

        # Navigation Buttons
        self.btn_canvas = ctk.CTkButton(
            self.sidebar,
            text="Air Canvas",
            command=lambda: self.set_mode("CANVAS")
            )
        self.btn_canvas.pack(pady=10, padx=20)

        self.btn_counter = ctk.CTkButton(
            self.sidebar,
            text="Finger Counter",
            command=lambda: self.set_mode("COUNTER")
            )
        self.btn_counter.pack(pady=10, padx=20)

        self.btn_system = ctk.CTkButton(
            self.sidebar,
            text="System Tools",
            command=lambda: self.set_mode("SYSTEM")
            )
        self.btn_system.pack(pady=10, padx=20)

        self.btn_clear = ctk.CTkButton(
            self.sidebar,
            text="Clear Canvas",
            fg_color="red",
            hover_color="#8B0000",
            command=self.clear_canvas
            )
        self.btn_clear.pack(side="bottom", pady=20, padx=20)

        # --- Main Video Display ---
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(expand=True, fill="both", padx=20, pady=20)

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector()
        self.engine = GestureEngine()
        self.canvas_app = AirCanvas()

        self.current_mode = "CANVAS"
        self.last_action_time = 0
        self.pinch_cooldown = 0
        self.fist_start_time = 0

        self.update_frame()

    def set_mode(self, mode):
        self.current_mode = mode
        print(f"Switched to {mode}")

    def clear_canvas(self):
        if self.current_mode == "CANVAS":
            self.canvas_app.canvas = None

    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=img_rgb
                )
            timestamp = int(time.time() * 1000)
            result = self.detector.find_hands(mp_image, timestamp)

            if result.hand_landmarks:
                landmarks = result.hand_landmarks[0]
                finger_state = self.engine.get_fingers_up(landmarks)

                dist = math.hypot(
                    landmarks[8].x - landmarks[4].x,
                    landmarks[8].y - landmarks[4].y
                    )

                if dist < 0.04 and (
                        time.time() - self.pinch_cooldown > 0.8):
                    self.pinch_cooldown = time.time()

                    if landmarks[
                        8].x < 0.3:
                        if landmarks[8].y < 0.3:
                            self.set_mode("CANVAS")
                        elif landmarks[8].y < 0.5:
                            self.set_mode("COUNTER")
                        elif landmarks[8].y < 0.8:
                            self.set_mode("SYSTEM")

                    cv2.circle(
                        frame,
                        (int(landmarks[8].x * w),
                         int(landmarks[8].y * h)),
                        20,
                        (0, 255, 0),
                        cv2.FILLED
                        )
                if self.current_mode == "CANVAS":
                    mode = self.engine.get_drawing_mode(finger_state)
                    frame = self.canvas_app.draw(frame, mode, landmarks)

                elif self.current_mode == "COUNTER":
                    count = finger_state.count(1)
                    cv2.putText(
                        frame, f"Fingers: {count}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4
                        )

                elif self.current_mode == "SYSTEM":
                    gesture = self.engine.get_system_gesture(landmarks)
                    current_time = time.time()
                    if current_time - self.last_action_time > 0.3:
                        if gesture == "THUMBS_UP":
                            pyautogui.press("volumeup")
                            self.last_action_time = current_time
                        elif gesture == "THUMBS_DOWN":
                            pyautogui.press("volumedown")
                            self.last_action_time = current_time

                    cv2.putText(
                        frame, f"System Active: {gesture}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2
                        )

                cursor_x = int(landmarks[8].x * w)
                cursor_y = int(landmarks[8].y * h)
                cv2.circle(
                    frame,
                    (cursor_x, cursor_y),
                    8,
                    (255, 255, 255),
                    -1
                    )

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(800, 500)
                )

            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk

        self.after(10, self.update_frame)


if __name__ == "__main__":
    app = VisionApp()
    app.mainloop()