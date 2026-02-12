# Hand Vision: Hand Tracking System

This project is a high-performance, real-time hand tracking application built with Python. It utilizes deep learning models to detect hand landmarks and interpret gestures, allowing users to interact with their computer through an "Air Canvas," finger counting, and system-level gesture controls (volume adjustment).

##  Features

* **Air Canvas:** Draw on your screen in real-time using your index finger. Includes a selection mode to move the cursor without drawing.
* **Finger Counter:** Accurately counts how many fingers are held up using landmark relative positioning.
* **System Tools:** Control your OS volume using "Thumbs Up" and "Thumbs Down" gestures.
* **Mode Switching:** A pinch-to-select gesture system that allows you to change application modes by touching specific regions of the screen.
* **Modern GUI:** Built with `CustomTkinter` for a sleek, dark-themed user interface.

##  Tech Stack & Requirements

The system is built using the following core technologies:

* **Python 3.9+**
* **MediaPipe:** Utilizes the `hand_landmarker.task` deep learning model for 21-point hand skeleton tracking.
* **OpenCV:** Handles video capture, frame processing, and image transformations.
* **CustomTkinter:** Provides the modern graphical user interface.
* **PyAutoGUI:** Enables the hand gestures to interact with the system (e.g., volume control).

### Prerequisites

Install the necessary dependencies via pip:

```bash
  pip install -r requirements.txt

```

## Project Structure

* `main.py`: The entry point containing the GUI logic and the main application loop.
* `modules/hand_detector.py`: Wraps MediaPipe's Landmarker for video-stream detection.
* `modules/gesture_engine.py`: Contains the logic for interpreting finger states and specific gestures.
* `controllers/aircanvas.py`: Manages the drawing logic and canvas overlays.
* `controllers/system.py`: Maps gestures to system actions like volume control.

##  How to Run

1. **Clone the Repository:**
```bash
  git clone https://github.com/varlamzhordania/ml_hand_tracking.git
  cd ml_hand_tracking
```

2. **Model Setup:**
Ensure the MediaPipe model file (`hand_landmarker.task`) is located in the `tasks/` directory.
3. **Launch the App:**
```bash
  python main.py

```



##  Gesture Guide

* **Mode Selection (The "Pinch"):** Bring your thumb and index finger together. While pinched, move your hand to the top-left area to switch modes.
* **Drawing (Canvas Mode):** Raise only your index finger to draw. Raise both index and middle fingers to move the cursor without drawing.
* **Volume Control (System Mode):** * **Thumbs Up:** Increase Volume.
* **Thumbs Down:** Decrease Volume.