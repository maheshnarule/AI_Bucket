
<img width="1920" height="923" alt="image" src="https://github.com/user-attachments/assets/345dd290-4f53-4021-aba7-61cb31b563d9" />
<img width="1920" height="922" alt="image" src="https://github.com/user-attachments/assets/0551f29d-d6ef-48d9-9da5-b9834b8d55fa" />
<img width="1901" height="915" alt="image" src="https://github.com/user-attachments/assets/c7e8c3eb-fce1-4bfa-978f-5643b8df3b14" />
<img width="1920" height="918" alt="image" src="https://github.com/user-attachments/assets/2e5817f3-a858-473e-a464-df3bae00a5a5" />
<img width="1910" height="896" alt="image" src="https://github.com/user-attachments/assets/2c581cac-3f7e-4b6c-ae35-c4248e54d52d" />
<img width="1920" height="909" alt="image" src="https://github.com/user-attachments/assets/82aa4424-55df-4ed7-92f8-ebf5a4b0e062" />
<img width="1920" height="909" alt="image" src="https://github.com/user-attachments/assets/7b158a3a-ad01-4ed3-9123-b7ab233079ae" />
<img width="1911" height="914" alt="image" src="https://github.com/user-attachments/assets/a666a2d0-0f0d-467f-bbf2-c55b0f809a47" />
<img width="1918" height="884" alt="image" src="https://github.com/user-attachments/assets/1cf03cff-acda-49bf-8625-73fc60b7ef2f" />
<img width="1905" height="930" alt="image" src="https://github.com/user-attachments/assets/7748adb5-5ef9-445a-97fc-40825d1ee151" />
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/4953ccb4-f4da-45f1-a166-6281b6bffc90" />
<img width="1920" height="905" alt="image" src="https://github.com/user-attachments/assets/94acc0f9-73de-462f-a115-a840777e7e69" />
Admin can see the User Data
<img width="1900" height="906" alt="image" src="https://github.com/user-attachments/assets/1a3e8e88-3bde-41bf-9fe1-7b4c47a627b8" />



**🧠 AI Bucket – Multi-Task Detection Project**

This project is an AI-powered web application built using Flask, OpenCV, and Deep Learning models.
It combines multiple computer vision and machine learning tasks into one platform.

**🚀 Features**

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

**🛠️ Tech Stack**

Frontend: HTML, CSS

Backend: Flask (Python)

Computer Vision: OpenCV

Deep Learning: TensorFlow / Keras, DeepFace, MediaPipe

**Models Used:**

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
│── user.py                # For creating Database for user data

│── README.md              # Project Documentation  

Use Python Version 3.10 for this Project in your system
⚡ Installation & Setup

**Clone the repository:**

git clone https://github.com/maheshnarule/AI_Bucket.git
cd AI_Bucket


**Install dependencies:**

pip install -r requirements.txt


**Run the application:**

python app.py


**Open in browser:**

http://127.0.0.1:5000/


**🔮 Future Enhancements**

Improve FPS with lightweight models.

Add more species for classification.

Support multi-face and multi-hand tracking simultaneously.

Deploy on cloud (Heroku / AWS).

