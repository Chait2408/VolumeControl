# Hand Tracking Volume Control

This project uses computer vision and hand tracking to control your system volume with hand gestures via your webcam. By measuring the distance between your thumb and index finger, you can increase or decrease the system volume in real time.

## Features

- Real-time hand detection and tracking using MediaPipe.
- Adjusts system volume based on the distance between thumb and index finger.
- Visual feedback with OpenCV (shows hand landmarks, volume bar, and FPS).
- Works on Windows (uses `pycaw` for system audio control).

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- opencv-python >= 4.5.0
- mediapipe >= 0.8.9
- numpy >= 1.19.0
- pycaw >= 20181226
- comtypes >= 1.1.10

## Usage

1. Make sure your webcam is connected.
2. Run the main script:

   ```bash
   python VolumeHandControl.py
   ```

3. A window will open showing your webcam feed. Use your thumb and index finger to control the volume:
   - Bring them close together to lower the volume.
   - Move them apart to increase the volume.
   - The volume bar and percentage will update in real time.
   - Press `q` to quit.

## File Overview

- `VolumeHandControl.py`: Main script for hand tracking and volume control.
- `HandTrackingModule.py`: Module for hand detection and landmark extraction using MediaPipe.
- `requirements.txt`: List of required Python packages.

## Notes

- This script is designed for Windows, as it uses `pycaw` for audio control.
- For best results, use in a well-lit environment. 