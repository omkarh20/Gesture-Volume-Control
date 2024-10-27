# Gesture Volume Control App

This project controls system volume based on hand gestures using OpenCV, Mediapipe, and Pycaw. By measuring the distance between two fingertips and calculating their relative size on-screen, the app estimates hand distance from the camera to adjust volume in real-time with a webcam feed.
The app dynamically updates based on hand distance, allowing more precise volume adjustments.

## Features

- **Real-time hand tracking** using Mediapipe
- **Dynamic volume control** based on hand gestures
- **Distance estimation** to adapt the minimum and maximum volume ranges as your hand distance changes
- **Visual feedback** on the screen to show volume percentage and FPS

## Demo

![Demo GIF](assets/volumeControlDemo.gif)

## Requirements

- **Python 3.x**
- **OpenCV** for handling image processing
- **Mediapipe** for hand detection and tracking
- **Pycaw** for system audio control

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gesture-volume-control.git
   cd gesture-volume-control
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```
2. Adjust the system volume by moving your thumb and index finger closer or further apart.
   
3. Press `ESC` to exit the app.

## Project Structure

- **main.py**: The main application file, handles webcam input, hand detection, and volume control.
- **HandTrackingModule.py**: A custom module for hand tracking using Mediapipe.

--- 
