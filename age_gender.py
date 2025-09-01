# import os
# import cv2
# from flask import render_template, request, Response
# from ag import faceBox, faceNet, ageNet, genderNet, ageList, genderList, MODEL_MEAN_VALUES
# from camera import get_camera   # ✅ Use get_camera, not capture_frame

# def register_age_gender_routes(app):

#     @app.route("/age_gender")
#     def age_gender_page():
#         return render_template("age_gender.html")

#     @app.route("/predict_age_gender", methods=["POST"])
#     def predict_age_gender():
#         if "file" not in request.files:
#             return render_template("age_gender.html", prediction="No file uploaded")

#         file = request.files["file"]
#         if file.filename == "":
#             return render_template("age_gender.html", prediction="No file selected")

#         filepath = os.path.join("uploads", file.filename)
#         os.makedirs("uploads", exist_ok=True)
#         file.save(filepath)

#         prediction = "No face detected"
#         try:
#             frame = cv2.imread(filepath)
#             frame, bboxs = faceBox(faceNet, frame)

#             if bboxs:  # if at least one face is found
#                 bbox = bboxs[0]  # take the first face
#                 face = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
#                 blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
#                                              MODEL_MEAN_VALUES, swapRB=False)

#                 # Gender prediction
#                 genderNet.setInput(blob)
#                 genderPred = genderNet.forward()
#                 gender = genderList[genderPred[0].argmax()]

#                 # Age prediction
#                 ageNet.setInput(blob)
#                 agePred = ageNet.forward()
#                 age = ageList[agePred[0].argmax()]

#                 prediction = f"Predicted Age: {age}, Gender: {gender}"

#         except Exception as e:
#             prediction = f"Error: {str(e)}"

#         finally:
#             if os.path.exists(filepath):
#                 os.remove(filepath)

#         return render_template("age_gender.html", prediction=prediction)
    
#     @app.route('/age_gender_camera')
#     def age_gender_camera():
#         return render_template("age_gender_camera.html")
    
#     # Live video generator
#     def gen_age_gender():
#         cap = get_camera()   # ✅ use global camera from camera.py
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame, bboxs = faceBox(faceNet, frame)
#             for bbox in bboxs:
#                 face = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
#                 blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
#                                              MODEL_MEAN_VALUES, swapRB=False)

#                 genderNet.setInput(blob)
#                 genderPred = genderNet.forward()
#                 gender = genderList[genderPred[0].argmax()]

#                 ageNet.setInput(blob)
#                 agePred = ageNet.forward()
#                 age = ageList[agePred[0].argmax()]

#                 label = f"{gender}, {age}"
#                 cv2.putText(frame, label, (bbox[0], bbox[1] - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             _, jpeg = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

#     @app.route('/video_feed_age_gender')
#     def video_feed_age_gender():
#         return Response(gen_age_gender(), mimetype='multipart/x-mixed-replace; boundary=frame')



import os
import cv2
from flask import render_template, request, Response
from deepface import DeepFace
from camera import get_camera

def register_age_gender_routes(app):

    # Page route
    @app.route("/age_gender")
    def age_gender_page():
        return render_template("age_gender.html")

    # Image upload and prediction
    @app.route("/predict_age_gender", methods=["POST"])
    def predict_age_gender():
        if "file" not in request.files:
            return render_template("age_gender.html", prediction="No file uploaded")

        file = request.files["file"]
        if file.filename == "":
            return render_template("age_gender.html", prediction="No file selected")

        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        prediction = "No face detected"
        try:
            result = DeepFace.analyze(
                img_path=filepath,
                actions=["age", "gender"],
                enforce_detection=False
            )

            r0 = result[0] if isinstance(result, list) else result
            age = int(r0.get("age", -1))
            gender = r0.get("dominant_gender", "Unknown")

            prediction = f"Predicted Age: {age}, Gender: {gender}"

        except Exception as e:
            prediction = f"Error: {str(e)}"

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        return render_template("age_gender.html", prediction=prediction)

    # Camera page
    @app.route('/age_gender_camera')
    def age_gender_camera():
        return render_template("age_gender_camera.html")

    # Live video generator with green rectangle
    def gen_age_gender():
        cap = get_camera()
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                results = DeepFace.analyze(
                    frame,
                    actions=["age", "gender"],
                    enforce_detection=False
                )

                if not isinstance(results, list):
                    results = [results]

                for r0 in results:
                    age = int(r0.get("age", -1))
                    gender = r0.get("dominant_gender", "Unknown")
                    region = r0.get("region", {})

                    # Draw green rectangle around the detected face
                    x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Put age + gender label above the box
                    label = f"{gender}, {age}"
                    cv2.putText(frame, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            except Exception:
                pass

            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    # Route for streaming
    @app.route('/video_feed_age_gender')
    def video_feed_age_gender():
        return Response(gen_age_gender(), mimetype='multipart/x-mixed-replace; boundary=frame')

