# 🚗 Driver Drowsiness Detection System

**👁️ Real-Time Eye Monitoring | 🧠 Computer Vision | 🔔 Smart Audio Alert**

A real-time **Driver Drowsiness Detection System** developed using **Python, OpenCV and MediaPipe Face Mesh**. This project monitors eye activity through a webcam and generates an audio alert when prolonged eye closure is detected.

The system supports both **dual-eye detection** when facing forward and **single-eye selection** during moderate left or right head turns.

---

## 📌 Project Overview

Driver fatigue and drowsiness can reduce attention and reaction time. This project demonstrates a computer vision-based approach to monitoring eye activity and identifying possible signs of drowsiness.

The system captures live video through a webcam, detects facial landmarks using MediaPipe Face Mesh and calculates the **Eye Aspect Ratio (EAR)** to monitor eye closure.

✨ An additional feature attempts to select the eye with the larger apparent width when the face turns sideways, allowing eye monitoring to continue when one eye is less visible.

When possible eye closure continues beyond a specified duration, the system displays a warning and triggers an audio alert.

---

## 🎯 Project Objectives

- 👤 Detect facial landmarks in real time.
- 👁️ Monitor eye movements using facial landmark information.
- 📐 Calculate the Eye Aspect Ratio (EAR).
- 🔄 Support both-eye and single-eye monitoring.
- 😴 Identify prolonged eye closure.
- 🔔 Generate an audio warning when possible drowsiness is detected.
- ⚡ Improve monitoring during moderate left and right head turns.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📷 Real-Time Monitoring | Captures live webcam video using OpenCV. |
| 👤 Face Landmark Detection | Detects facial landmarks using MediaPipe Face Mesh. |
| 👀 Dual-Eye Detection | Uses both eyes when facing the camera. |
| ↔️ Single-Eye Selection | Attempts to select the eye with the larger apparent width during sideways turns. |
| 📐 EAR Calculation | Calculates eye openness using facial landmark distances. |
| ⚙️ Automatic Calibration | Establishes an initial eye-open baseline. |
| 📊 EAR Smoothing | Uses a rolling median to reduce sudden measurement fluctuations. |
| ⏱️ Closure Confirmation | Checks whether possible eye closure continues for approximately 3 seconds. |
| 🔊 Audio Alert | Plays an audible warning using Python's `winsound`. |
| 🖥️ Live Status Display | Displays EAR, threshold, detected eye and monitoring status. |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python 3.12 | Main programming language |
| 📷 OpenCV | Webcam access and image processing |
| 🧠 MediaPipe Face Mesh | Facial landmark detection |
| 🔢 NumPy / Python Statistics | Numerical and measurement processing |
| 🔔 Winsound | Audio alert generation |
| 📦 UV | Python package and environment management |

---

## 🧠 Working Principle

### 1️⃣ Webcam Capture 📷

OpenCV captures live video frames from the webcam and prepares them for facial landmark processing.

### 2️⃣ Face Landmark Detection 👤

MediaPipe Face Mesh identifies facial landmarks, including important points around both eyes.

### 3️⃣ Dual-Eye and Single-Eye Selection 👀

The system uses two eye-monitoring approaches:

- **Facing Forward:** Calculates EAR using both eyes.
- **Turning Left or Right:** Compares the apparent widths of both eyes and attempts to select the eye with the larger apparent width.

This helps maintain eye monitoring when one eye becomes less visible during moderate head turns.

### 4️⃣ Eye Aspect Ratio (EAR) Calculation 📐

EAR measures the relationship between the vertical and horizontal dimensions of the eye.

The mathematical expression is:

\[
EAR = \frac{d_1+d_2}{2d_3}
\]

Where:

- \(d_1\) and \(d_2\) represent vertical eye landmark distances.
- \(d_3\) represents horizontal eye landmark distance.

A lower EAR value can indicate possible eye closure.

### 5️⃣ Calibration and Smoothing ⚙️

The system collects initial eye-open measurements to establish a baseline.

A rolling median filter smooths the EAR measurements to reduce sudden fluctuations and improve monitoring stability.

### 6️⃣ Drowsiness Detection 😴

The smoothed EAR value is compared with a calibrated threshold.

If the EAR remains below the threshold for approximately three seconds, the system identifies possible prolonged eye closure.

### 7️⃣ Audio Alert 🔔

When the confirmation condition is satisfied, the system displays a warning message and activates an audible alarm.

---

## 🔄 System Workflow

```text
       🚀 START
          |
          v
    📷 Open Webcam
          |
          v
   👤 Detect Face Landmarks
          |
          v
   👀 Identify Eye Landmarks
          |
          v
   ↔️ Select Monitoring Method
          |
     +----+----+
     |         |
  Both Eyes  Single Eye
     |         |
     +----+----+
          |
          v
     📐 Calculate EAR
          |
          v
     ⚙️ Smooth EAR Values
          |
          v
      ⏱️ Check Duration
          |
     +----+----+
     |         |
  Eyes Open  Possible
             Closure
     |         |
     |         v
     |    ⏳ Confirm 3 Seconds
     |         |
     |         v
     |     🔔 Audio Alert
     |         |
     +----+----+
          |
          v
    🖥️ Display Status
          |
          v
      🔁 Repeat
```

---

## 📂 Project Structure

```text
Driver-Drowsiness-Detection/
│
├── 📁 models/
│
├── 📁 src/
│   └── __init__.py
│
├── 🐍 drowsiness_detection.py
├── 📦 pyproject.toml
├── 🔒 uv.lock
├── ⚙️ .python-version
├── 🚫 .gitignore
└── 📖 README.md
```

---

## ⚙️ Installation and Setup

### 📋 Prerequisites

- Windows operating system
- Python 3.12
- Visual Studio Code
- Webcam
- Speakers
- UV package manager

### Step 1: Clone the Repository 📥

```bash
git clone https://github.com/jewinjoy63-ops/Driver-Drowsiness-Detection.git
```

### Step 2: Open the Project Folder 📂

```bash
cd Driver-Drowsiness-Detection
```

### Step 3: Install Dependencies 📦

```bash
uv sync
```

### Step 4: Run the Application ▶️

```bash
uv run python drowsiness_detection.py
```

### Step 5: Exit the Application ⏹️

Press **Q** to close the webcam window.

---

## 🖥️ Expected System Output

The webcam window displays:

- 🟢 Eye status
- 👀 Detected eye information
- 📊 Current EAR value
- 📐 EAR threshold
- 🔴 Possible drowsiness warning

---

## 🔮 Future Enhancements

- 🎯 Improve eye visibility estimation.
- 🧭 Introduce head-pose-aware EAR calibration.
- 🥱 Add yawning detection.
- 💡 Improve detection under different lighting conditions.
- 📊 Add a graphical user interface.
- 📈 Evaluate detection performance using different camera positions.
- 🔔 Explore additional alert mechanisms.

---

## ⚠️ Limitations and Disclaimer

- Single-eye selection is based on apparent eye width and does not guarantee actual eye visibility.
- Detection accuracy may decrease during sharp head turns or partial eye obstruction.
- EAR thresholds can vary between individuals and camera positions.
- This project is an educational prototype, not a certified driver-safety system.

**🚨 Important:** This application is developed for educational and demonstration purposes only. It must not replace professional driver-safety systems or be relied upon to determine whether someone is safe to drive.

---

## 👨‍💻 Author

**Jewinjoy63-ops**

💻 Python | 🤖 Artificial Intelligence | 👁️ Computer Vision

🔗 **GitHub Profile:** [@jewinjoy63-ops](https://github.com/jewinjoy63-ops)

📁 **Project Repository:** [Driver Drowsiness Detection](https://github.com/jewinjoy63-ops/Driver-Drowsiness-Detection)

---

## 📜 License

No license has currently been added to this repository. All rights are reserved by the author unless a license is added.

---

### ⭐ Support the Project

If you find this project interesting, consider giving the repository a star!

🚗 **Building smarter computer vision applications for safer driving awareness.**