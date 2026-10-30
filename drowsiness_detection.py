
import cv2
import time
import winsound
import mediapipe as mp
from pathlib import Path

# Model file
MODEL_PATH = Path(__file__).parent / "models" / "face_landmarker.task"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

# MediaPipe configuration
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=RunningMode.VIDEO,
    num_faces=1,
    min_face_detection_confidence=0.4,
    min_face_presence_confidence=0.4,
    min_tracking_confidence=0.4
)

CONFIRM_SECONDS = 3.0
ALARM_COOLDOWN = 5.0

missing_eyes_start = None
last_alarm = 0.0
frame_timestamp_ms = 0

# Approximate eye landmark points
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


def eye_aspect_ratio(landmarks, indices):
    points = [
        (landmarks[i].x, landmarks[i].y)
        for i in indices
    ]

    import math

    def distance(a, b):
        return math.dist(a, b)

    vertical1 = distance(points[1], points[5])
    vertical2 = distance(points[2], points[4])
    horizontal = distance(points[0], points[3])

    if horizontal == 0:
        return 0.0

    return (vertical1 + vertical2) / (2.0 * horizontal)


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

try:
    with FaceLandmarker.create_from_options(options) as landmarker:
        while True:
            success, frame = cap.read()

            if not success:
                print("Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            frame_timestamp_ms += 33
            result = landmarker.detect_for_video(
                mp_image, frame_timestamp_ms
            )

            status = "Face not visible"
            color = (0, 165, 255)

            if result.face_landmarks:
                landmarks = result.face_landmarks[0]

                # Draw facial landmark points
                for point in landmarks:
                    px = int(point.x * width)
                    py = int(point.y * height)

                    if 0 <= px < width and 0 <= py < height:
                        cv2.circle(
                            frame, (px, py), 1, (0, 255, 0), -1
                        )

                left_ear = eye_aspect_ratio(
                    landmarks, LEFT_EYE
                )
                right_ear = eye_aspect_ratio(
                    landmarks, RIGHT_EYE
                )
                ear = (left_ear + right_ear) / 2.0

                # Initial demo threshold; requires calibration
                EYE_CLOSED_THRESHOLD = 0.18

                if ear < EYE_CLOSED_THRESHOLD:
                    if missing_eyes_start is None:
                        missing_eyes_start = time.monotonic()

                    duration = (
                        time.monotonic() - missing_eyes_start
                    )

                    if duration >= CONFIRM_SECONDS:
                        status = "WARNING: EYES MAY BE CLOSED"
                        color = (0, 0, 255)

                        now = time.monotonic()
                        if now - last_alarm >= ALARM_COOLDOWN:
                            winsound.Beep(1500, 5000)
                            last_alarm = time.monotonic()
                    else:
                        status = "Checking eye closure..."
                        color = (0, 165, 255)
                else:
                    missing_eyes_start = None
                    status = f"Eyes open - EAR: {ear:.2f}"
                    color = (0, 255, 0)

            else:
                # Missing face landmarks are not proof of drowsiness
                missing_eyes_start = None

            cv2.putText(
                frame,
                status,
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                color,
                2
            )

            cv2.imshow(
                "MediaPipe Driver Monitoring - Prototype",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
