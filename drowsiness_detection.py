
import cv2
import time
import winsound
import mediapipe as mp
import math
import threading
import statistics

from collections import deque

# -----------------------------------------
# CONFIGURATION
# -----------------------------------------

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

CONFIRM_SECONDS = 3.0
ALARM_DURATION = 5000
ALARM_COOLDOWN = 6.0

CALIBRATION_SECONDS = 3.0
SMOOTHING_FRAMES = 5

EYE_CLOSED_THRESHOLD = 0.18

# -----------------------------------------
# EYE LANDMARK INDICES
# -----------------------------------------

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# -----------------------------------------
# VARIABLES
# -----------------------------------------

smooth_values = deque(maxlen=SMOOTHING_FRAMES)
calibration_values = []

calibration_start = time.monotonic()
calibrated = False

missing_eyes_start = None
last_alarm = 0.0
alarm_playing = False

# -----------------------------------------
# EYE ASPECT RATIO
# -----------------------------------------


def eye_aspect_ratio(landmarks, indices, width, height):

    points = [
        (landmarks[i].x * width, landmarks[i].y * height)
        for i in indices
    ]

    vertical1 = math.dist(points[1], points[5])
    vertical2 = math.dist(points[2], points[4])
    horizontal = math.dist(points[0], points[3])

    if horizontal < 1:
        return 0.0

    return (vertical1 + vertical2) / (2.0 * horizontal)


def get_visible_eye_ear(landmarks, width, height):

    left_width = math.dist(
        (landmarks[362].x * width, landmarks[362].y * height),
        (landmarks[263].x * width, landmarks[263].y * height)
    )

    right_width = math.dist(
        (landmarks[33].x * width, landmarks[33].y * height),
        (landmarks[133].x * width, landmarks[133].y * height)
    )

    # Select the eye with the larger apparent width
    # when the face is turned sideways.
    smaller = min(left_width, right_width)
    larger = max(left_width, right_width)

    if larger < 5:
        return None, "No reliable eye"

    if smaller / larger < 0.75:

        if left_width > right_width:
            return (
                eye_aspect_ratio(
                    landmarks, LEFT_EYE, width, height
                ),
                "Left eye"
            )

        return (
            eye_aspect_ratio(
                landmarks, RIGHT_EYE, width, height
            ),
            "Right eye"
        )

    left_ear = eye_aspect_ratio(
        landmarks, LEFT_EYE, width, height
    )

    right_ear = eye_aspect_ratio(
        landmarks, RIGHT_EYE, width, height
    )

    return (left_ear + right_ear) / 2.0, "Both eyes"

# -----------------------------------------
# ALARM FUNCTION
# -----------------------------------------

def play_alarm():

    global alarm_playing

    try:
        winsound.Beep(1500, ALARM_DURATION)

    finally:
        alarm_playing = False


def start_alarm():

    global alarm_playing, last_alarm

    now = time.monotonic()

    if (
        not alarm_playing
        and now - last_alarm >= ALARM_COOLDOWN
    ):

        alarm_playing = True
        last_alarm = now

        threading.Thread(
            target=play_alarm,
            daemon=True
        ).start()


# -----------------------------------------
# CAMERA SETUP
# -----------------------------------------

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

WINDOW_NAME = "Driver Drowsiness Detection"

cv2.namedWindow(
    WINDOW_NAME,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    WINDOW_NAME,
    900,
    750
)

if not cap.isOpened():

    raise RuntimeError(
        "Could not open webcam."
    )


# -----------------------------------------
# MEDIAPIPE FACE MESH
# -----------------------------------------

try:

    with mp.solutions.face_mesh.FaceMesh(

        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,

        min_detection_confidence=0.5,
        min_tracking_confidence=0.6

    ) as face_mesh:

        while True:

            success, frame = cap.read()

            if not success:

                print("Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)

            height, width = frame.shape[:2]

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = face_mesh.process(rgb)

            status = "Face not detected"
            color = (0, 165, 255)

            # ---------------------------------
            # FACE DETECTION
            # ---------------------------------

            if results.multi_face_landmarks:

                landmarks = (
                    results.multi_face_landmarks[0].landmark
                )

                # Get EAR from available eye(s)
                ear, detected_eye = get_visible_eye_ear(
                    landmarks , width, height
                )

                # Draw eye landmark points
                for eye_indices in [LEFT_EYE, RIGHT_EYE]:

                    for index in eye_indices:

                        point = landmarks[index]

                        px = int(point.x * width)
                        py = int(point.y * height)

                        if (
                            0 <= px < width
                            and 0 <= py < height
                        ):

                            cv2.circle(
                                frame,
                                (px, py),
                                2,
                                (0, 255, 0),
                                -1
                            )

                # ---------------------------------
                # EYE NOT RELIABLY DETECTED
                # ---------------------------------

                if ear is None:

                    missing_eyes_start = None
                    smooth_values.clear()

                    status = "Eyes not clearly detected"
                    color = (0, 165, 255)

                else:

                    smooth_values.append(ear)

                    smooth_ear = statistics.median(
                        smooth_values
                    )

                    # ---------------------------------
                    # CALIBRATION
                    # ---------------------------------

                    if not calibrated:

                        if smooth_ear > 0.12:

                            calibration_values.append(
                                smooth_ear
                            )

                        elapsed = (
                            time.monotonic()
                            - calibration_start
                        )

                        if elapsed >= CALIBRATION_SECONDS:

                            if len(calibration_values) >= 10:

                                baseline = statistics.median(
                                    calibration_values
                                )

                                EYE_CLOSED_THRESHOLD = max(
                                    0.15,
                                    min(0.25, baseline * 0.72)
                                )

                            calibrated = True

                        else:

                            status = "Calibrating - Keep eyes open"
                            color = (255, 200, 0)

                    # ---------------------------------
                    # DROWSINESS DETECTION
                    # ---------------------------------

                    if calibrated:

                        if smooth_ear < EYE_CLOSED_THRESHOLD:

                            if missing_eyes_start is None:

                                missing_eyes_start = (
                                    time.monotonic()
                                )

                            duration = (
                                time.monotonic()
                                - missing_eyes_start
                            )

                            if duration >= CONFIRM_SECONDS:

                                status = "WARNING: POSSIBLE DROWSINESS"
                                color = (0, 0, 255)

                                start_alarm()

                            else:

                                status = "Checking eye closure..."
                                color = (0, 165, 255)

                        elif smooth_ear > EYE_CLOSED_THRESHOLD + 0.03:

                            missing_eyes_start = None

                            status = "Eyes open"
                            color = (0, 255, 0)

                        else:

                            status = "Monitoring eyes..."
                            color = (0, 165, 255)

                    # ---------------------------------
                    # DISPLAY EAR INFORMATION
                    # ---------------------------------

                    cv2.putText(
                        frame,
                        f"EAR: {smooth_ear:.3f}",
                        (15, 95),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Detected: {detected_eye}",
                        (15, 65),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Threshold: {EYE_CLOSED_THRESHOLD:.3f}",
                        (15, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

            else:

                missing_eyes_start = None
                smooth_values.clear()

            # ---------------------------------
            # DISPLAY STATUS
            # ---------------------------------

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
                WINDOW_NAME,
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


finally:

    cap.release()
    cv2.destroyAllWindows()

