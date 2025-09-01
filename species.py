
import os
import cv2
import numpy as np
from flask import render_template, request, Response
from tensorflow.keras.applications.resnet50 import ResNet50, decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from camera import get_camera   # ✅ Import shared camera

species_model = ResNet50(weights="imagenet")

def register_species_routes(app):

    # ========== IMAGE UPLOAD & PREDICTION ==========
    @app.route('/species', methods=["GET", "POST"])
    def species_upload():
        prediction = None
        if request.method == "POST":
            if "file" not in request.files:
                return render_template("species.html", prediction="No file uploaded")

            file = request.files["file"]
            if file.filename == "":
                return render_template("species.html", prediction="No file selected")

            filepath = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(filepath)

            # Preprocess image
            img = image.load_img(filepath, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Prediction
            preds = species_model.predict(x)
            decoded = decode_predictions(preds, top=3)[0]

            prediction = "Predictions:<br>"
            for i, (_, label, prob) in enumerate(decoded):
                prediction += f"{i+1}. {label} ({prob*100:.2f}%)<br>"

            os.remove(filepath)

        return render_template("species.html", prediction=prediction)

    # ========== CAMERA PAGE ==========
    @app.route('/species_camera')
    def species_camera():
        return render_template("species.html")

    # ========== LIVE CAMERA DETECTION ==========
    def gen_frames():
        cap = get_camera()  # ✅ Shared camera
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Preprocess frame
            img = cv2.resize(frame, (224, 224))
            x = np.expand_dims(img, axis=0)
            x = preprocess_input(x)

            preds = species_model.predict(x)
            decoded = decode_predictions(preds, top=1)[0]
            label = f"{decoded[0][1]} ({decoded[0][2]*100:.2f}%)"

            # Show label on frame
            cv2.putText(frame, label, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed_species')
    def video_feed_species():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
