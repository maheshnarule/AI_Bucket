import os
import cv2
from flask import render_template, request, Response
from deepface import DeepFace
from camera import capture_frame   # ✅ use capture_frame only


def register_emotion_routes(app):

    @app.route("/emotion")
    def emotion_page():
        return render_template("emotion.html")

    # Upload image for emotion detection
    @app.route("/emotion_upload", methods=["POST"])
    def emotion_upload():
        prediction = None
        if "file" not in request.files:
            return render_template("emotion.html", prediction="No file uploaded")

        file = request.files["file"]
        if file.filename == "":
            return render_template("emotion.html", prediction="No file selected")

        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        try:
            result = DeepFace.analyze(img_path=filepath, actions=["emotion"], enforce_detection=False)
            emotion = result[0]["dominant_emotion"]
            prediction = f"Predicted Emotion: {emotion}"
        except Exception as e:
            prediction = f"Error: {str(e)}"

        os.remove(filepath)
        return render_template("emotion.html", prediction=prediction)
    
    @app.route('/emotion_camera')
    def emotion_camera():
        return render_template("emotion_camera.html")

    # Live emotion detection
    def gen_emotion():
        while True:
            frame = capture_frame()   # ✅ get frame directly from camera.py
            if frame is None:
                continue
            try:
                results = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                emotion = results[0]['dominant_emotion']
                cv2.putText(frame, f"Emotion: {emotion}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            except:
                pass

            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    @app.route('/video_feed_emotion')
    def video_feed_emotion():
        return Response(gen_emotion(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
