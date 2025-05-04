# 🎮 Hand-Controlled Snake Game 🖐️🐍

My first exploration in the field of Computer Vision!

In this game, you control the classic Snake 🐍 using only your **hand gestures**, powered by **MediaPipe** and **Pygame**.  
No keyboard or mouse is needed—just your hand!

---

## ✨ Features

- 🖐️ **Hand Tracking**: Control the snake with your hand using the **MediaPipe** hand tracking API.
- 🕹️ **Pygame Integration**: Play on a Pygame-rendered screen with all the classic Snake action.
- 🧠 **Intuitive Gesture Logic**: Your hand position (relative to screen center) determines snake movement direction.
- 🚫 **No Keyboard Required**: Just move your hand to steer—no buttons or keys involved!
- 🐍 **Classic Snake Mechanics**: Eat food to grow longer, and avoid colliding with yourself or walls!
- 🧪 **Multithreading**: Separates hand tracking and game rendering into two smooth concurrent threads.
- 🔄 **Dynamic Difficulty Potential**: You can easily adapt snake speed, thresholds, or control logic for unique variations.

---

## 🛠️ How It Works

The game uses two main components:

1. **MediaPipe** (via OpenCV) tracks your hand in real-time using the webcam.
2. **Pygame** renders the game and responds to directional cues based on your hand’s position.

A background thread constantly updates the position of your index finger (landmark 8), and the game loop adjusts movement based on where your finger is on the screen.

---

## 🧱 Requirements

Make sure you have the following Python libraries installed:

```bash
pip install opencv-python mediapipe pygame
