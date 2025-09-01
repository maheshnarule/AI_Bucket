

import cv2

# Global camera object
camera = cv2.VideoCapture(0)

def get_camera():
    global camera
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)
    return camera

def capture_frame():
    global camera
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        return frame
    return None





