# 🚗 Driver Drowsiness Detection System

A real-time Driver Drowsiness Detection System developed using **Python, OpenCV and MediaPipe Face Mesh**. The system monitors the driver's eyes through a webcam and generates an audio alert when prolonged eye closure is detected.

## 📌 Project Overview

Driver fatigue and drowsiness can reduce attention and reaction time. This project demonstrates a computer vision-based approach to monitoring eye activity and identifying possible signs of drowsiness.

The system captures video through a webcam, detects facial landmarks using MediaPipe Face Mesh and calculates the Eye Aspect Ratio (EAR) to monitor eye closure.

When eye closure continues beyond a specified time, an audio warning is triggered.

## 🎯 Objectives

- Detect facial landmarks in real time.
- Monitor eye movements using facial landmark information.
- Calculate Eye Aspect Ratio (EAR).
- Identify prolonged eye closure.
- Generate an audio warning when possible drowsiness is detected.

## ✨ Features

- Real-time webcam monitoring.
- Face detection using MediaPipe Face Mesh.
- Eye landmark visualization.
- Eye Aspect Ratio (EAR) calculation.
- Configurable eye-closure detection threshold.
- Three-second eye-closure confirmation.
- Audio warning using Python's `winsound`.
- Live status display on the webcam window.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| OpenCV | Webcam access and image processing |
| MediaPipe Face Mesh | Facial landmark detection |
| NumPy | Numerical processing |
| Winsound | Audio warning |

## 🧠 Working Principle

### 1. Webcam Capture
The webcam captures live video frames using OpenCV.

### 2. Face Landmark Detection
MediaPipe Face Mesh identifies facial landmarks, including points around the eyes.

### 3. Eye Aspect Ratio (EAR)
The system calculates the Eye Aspect Ratio to estimate whether the eyes are open or closed.

The mathematical expression is:

\[
EAR = \frac{d_1+d_2}{2d_3}
\]

Where:

- \(d_1\) and \(d_2\) represent vertical eye distances.
- \(d_3\) represents horizontal eye distance.

### 4. Drowsiness Detection
When the EAR falls below the configured threshold, the system checks how long the eyes remain closed.

### 5. Audio Alert
If eye closure continues for approximately three seconds, the system displays a warning and plays an audio alert.

## 📂 Project Structure

```text
Driver-Drowsiness-Detection/
│
├── models/
├── src/
│   └── __init__.py
│
├── drowsiness_detection.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Windows operating system
- Python 3.12
- Webcam
- Speakers
- UV package manager

### Step 1: Clone the repository

```bash
git clone https://github.com/jewinjoy63-ops/Driver-Drowsiness-Detection.git
```

### Step 2: Open the project folder

```bash
cd Driver-Drowsiness-Detection
```

### Step 3: Install dependencies

```bash
uv sync
```

### Step 4: Run the application

```bash
uv run python drowsiness_detection.py
```

### Step 5: Exit the application

Press `Q` to close the webcam window.

## 🔮 Future Enhancements

- Head pose estimation.
- Yawning detection.
- Improved detection under different lighting conditions.
- Graphical user interface.
- Detection performance evaluation.
- More advanced alert mechanisms.

## ⚠️ Disclaimer

This project is an educational prototype developed for learning computer vision and real-time monitoring. It is not a certified driver-safety system and should not be relied upon to prevent accidents or determine whether someone is safe to drive.

## 👨‍💻 Author

**Jewinjoy63-ops**

GitHub: [@jewinjoy63-ops](https://github.com/jewinjoy63-ops)

## 📜 License

No license has currently been added to this repository. All rights are reserved by the author unless a license is added.
