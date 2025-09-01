🧠 AI Bucket – Multi-Task Detection Project

This project is an AI-powered web application built using Flask, OpenCV, and Deep Learning models.
It combines multiple computer vision and machine learning tasks into one platform.

🚀 Features

✅ Age & Gender Detection

Detects faces from the webcam.

Predicts age group and gender using pre-trained deep learning models.

✅ Emotion Recognition

Identifies human emotions (Happy, Sad, Angry, Surprise, Neutral, etc.).

Real-time predictions with bounding boxes on faces.

✅ Hand Gesture Detection

Detects hand gestures from webcam input.

Recognizes common gestures for interactive use cases.

✅ Species Classification

Image upload system to classify object species (Dog, pen, water Bottle etc.).

Uses deep learning .h5 model for classification.

🛠️ Tech Stack

Frontend: HTML, CSS

Backend: Flask (Python)

Computer Vision: OpenCV

Deep Learning: TensorFlow / Keras, DeepFace, MediaPipe

Models Used:

Age & Gender Detection Model (.h5)

Emotion Recognition Model (.h5)

Hand Gesture Detection Model

Species Classification Model

📂 Project Structure
AI_Bucket/
│── app.py                 # Main Flask app  
│── age_gender.py          # Age & Gender Detection routes  
│── emotion.py             # Emotion Recognition routes  
│── hand_gesture.py        # Hand Gesture Detection routes  
│── species.py             # Species Classification routes 
│── camera.py              # Global Camera 
│── templates/             # HTML templates (index, dashboard, etc.)                 
│── requirements.txt       # Dependencies  
│── user.db                # Database for user data
│── README.md              # Project Documentation  

Use Python Version 3.10 for this Project in your system
⚡ Installation & Setup

Clone the repository:

git clone https://github.com/maheshnarule/AI_Bucket.git
cd AI_Bucket


Install dependencies:

pip install -r requirements.txt


Run the application:

python app.py


Open in browser:

http://127.0.0.1:5000/


🔮 Future Enhancements

Improve FPS with lightweight models.

Add more species for classification.

Support multi-face and multi-hand tracking simultaneously.

Deploy on cloud (Heroku / AWS).

Author

GitHub: @maheshnarule

