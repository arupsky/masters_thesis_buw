import cv2

eye_cascade = cv2.CascadeClassifier('eye.xml')
print(eye_cascade)

def detect_eye(image):
    eye = eye_cascade.detectMultiScale(image)
    if len(eye)>=1:
        return True
    return False