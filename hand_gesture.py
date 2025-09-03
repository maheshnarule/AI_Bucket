
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
        Returns hand label (Left/Right) and finger states [Thumb..Pinky].
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

        return handedness, [int(f) for f in fingers]  # Convert bools → 0/1

    def recognize_gesture(fingers):
        """
        Recognize gestures from finger states.
        fingers: [Thumb, Index, Middle, Ring, Pinky] as 0/1
        """
        gestures = {
            (0,0,0,0,0): "✊ Fist",
            (1,1,1,1,1): "🖐️ Open Palm",
            (0,1,0,0,0): "☝️ Point",
            (0,1,1,0,0): "✌️ Victory",
            (1,1,0,0,0): "👌 OK",
            (0,0,0,0,1): "Pinky 🤙",
            (1,0,0,0,0): "👍 Thumbs Up",
            (0,0,0,0,1): "👎 Thumbs Down",
            (0,1,1,1,1): "✋ Four Fingers",
            (0,1,1,1,0): "Three Fingers",
            (0,1,0,1,0): "Peace Variant",
            (1,1,1,0,0): "Three (Thumb+Index+Middle)",
            (1,0,1,0,0): "Gun 🔫",
            (1,0,0,1,1): "Spider-Man 🤟",
            (1,1,0,0,1): "Shaka 🤙",
            (0,0,1,1,1): "Last Three Fingers",
            (0,1,0,0,1): "Index+Pinky ✌️",
            (1,0,1,1,1): "All but Index",
            (0,1,1,0,1): "Index+Middle+Pinky",
            (1,1,1,1,0): "All but Pinky",
            (1,1,0,0,1): "🤏 Pinch"
        }

        return gestures.get(tuple(fingers), f" Unknown {fingers}")

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

            gesture_text = "No Hand"

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    hand_label = hand_handedness.classification[0].label  # Left/Right
                    hand_label, fingers = hand_label_and_fingers(hand_landmarks, hand_label)

                    fingers_count = sum(fingers)
                    gesture_text = recognize_gesture(fingers)

                    # Use wrist landmark for placing hand info
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    h, w, _ = frame.shape
                    x_pos = int(wrist.x * w)
                    y_pos = int(wrist.y * h) - 30  # Slightly above wrist

                    cv2.putText(frame, f"{hand_label} Hand", (x_pos, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(frame, f"Fingers: {fingers_count}", (x_pos, y_pos + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # 🔹 Always show gesture name in top-left corner
            cv2.putText(frame, f"Gesture: {gesture_text}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

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
