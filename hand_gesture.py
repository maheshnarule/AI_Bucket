

import cv2
import mediapipe as mp
from flask import render_template, Response
from camera import get_camera  # ✅ use get_camera from camera.py

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)


def register_hand_routes(app):

    @app.route("/hand_gesture")
    def hand_gesture():
        return render_template("hand_gesture.html")

    def hand_label_and_fingers(hand_landmarks, handedness):
        """
        Returns hand label (Left/Right) and count of raised fingers.
        """
        tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        fingers = []

        # Thumb
        if handedness == "Right":
            fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
        else:  # Left hand
            fingers.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)

        # Other 4 fingers
        for tip in tips_ids[1:]:
            fingers.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)

        count = fingers.count(True)
        return handedness, count

    def generate_hand_gestures():
        cap = get_camera()
        while True:
            success, frame = cap.read()
            if not success:
                break

            # 🔹 Flip frame horizontally for mirror view
            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    hand_label = hand_handedness.classification[0].label  # Left/Right
                    hand_label, fingers_count = hand_label_and_fingers(hand_landmarks, hand_label)

                    # Use wrist landmark for placing text
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    h, w, _ = frame.shape
                    x_pos = int(wrist.x * w)
                    y_pos = int(wrist.y * h) - 30  # Slightly above wrist

                    cv2.putText(frame, f"{hand_label} Hand", (x_pos, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(frame, f"Fingers: {fingers_count}", (x_pos, y_pos + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    @app.route('/gesture_camera')
    def gesture_camera():
        return render_template("gesture_camera.html")

    @app.route("/camera_hand")
    def camera_hand():
        return Response(generate_hand_gestures(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
