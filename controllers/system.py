import pyautogui
from controllers.basic import AppController


class SystemController(AppController):
    def react(self, gesture):
        if gesture == "THUMBS_UP":
            pyautogui.press("volumeup")
        elif gesture == "THUMBS_DOWN":
            pyautogui.press("volumedown")
        elif gesture == "FIST":
            pyautogui.press("space")
