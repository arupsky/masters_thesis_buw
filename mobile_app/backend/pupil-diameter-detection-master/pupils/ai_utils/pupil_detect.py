from cv2 import cv2
# import tensorflow as tf
from . import detect_eye
# from .face_detector import MTCNNFaceDetector
# # from .elg_keras import KerasELG
# from keras import backend as K
# from keras.backend import set_session
import numpy as np
from firebase_admin import storage

mtcnn_weights_dir = "./mtcnn_weights/"
# sess = K.get_session()
# set_session(sess)
# fd = MTCNNFaceDetector(sess=sess, model_path=mtcnn_weights_dir)
# print('model',fd)
# model = KerasELG()
# model.net.load_weights("./elg_weights/elg_keras.h5")

# print(model)
def detect_face_and_eye(input_img,fd,distance=None):
    face, lms = fd.detect_face(input_img)
    if len(face)==0:
        print('no face detected')
        return 0
    left_eye_xy = np.array([lms[6], lms[1]])
    right_eye_xy = np.array([lms[5], lms[0]])
    dist_eyes = np.linalg.norm(left_eye_xy - right_eye_xy)
    eye_bbox_w = (dist_eyes / 1.25)
    eye_bbox_h = (eye_bbox_w * 0.6)
    left_eye_im = input_img[
                  int(left_eye_xy[0] - eye_bbox_h // 2):int(left_eye_xy[0] + eye_bbox_h // 2),
                  int(left_eye_xy[1] - eye_bbox_w // 2):int(left_eye_xy[1] + eye_bbox_w // 2), :]
    # left_eye_im = left_eye_im[:,::-1,:] # No need for flipping left eye for iris detection
    right_eye_im = input_img[
                   int(right_eye_xy[0] - eye_bbox_h // 2):int(right_eye_xy[0] + eye_bbox_h // 2),
                   int(right_eye_xy[1] - eye_bbox_w // 2):int(right_eye_xy[1] + eye_bbox_w // 2), :]


    is_left_eye_open = detect_eye(left_eye_im)
    is_right_eye_open = detect_eye(right_eye_im)

    if is_left_eye_open and is_right_eye_open:
        diameter = calculate_pupil_diameter(input_img,left_eye_xy,right_eye_xy)
        if distance:
            diameter = diameter*distance
        return diameter

    return 0



def calculate_pupil_diameter(input_img,left_pupil_point,right_pupil_point):
    xl = int(left_pupil_point[0])
    yl = int(left_pupil_point[1])
    xr = int(right_pupil_point[0])
    yr = int(right_pupil_point[1])
    tl=xl
    tr=xr
    d=1
    for i in range(25):
        # print('real : ',input_img[xl][yl], input_img[xr][yr])
        # print('temp: ',input_img[tl][yl], input_img[tr][yr])
        xl -= 1
        xr -= 1
        val_left , val_right = input_img[xl][yl][0] , input_img[xr][yr][0]

        if input_img[xl][yl][0]>80 or input_img[xl][yl][1]>80 or input_img[xl][yl][2]>80 \
            or input_img[xr][yr][0] >80 or input_img[xr][yr][1] >80 or input_img[xr][yr][2] >80 :
            break
        d += 1
        tl -=2
        tr -=2


    diameter = d*0.2645

    if d <= 10:
        return 0.2645*10

    return diameter


def get_image_from_firebase(img_url):
    img_url = 'images/'+img_url
    blob = storage.bucket()
    b_ob = blob.get_blob(img_url)
    arr = np.frombuffer(b_ob.download_as_string(), np.uint8)
    # arr = np.asarray(b_ob.download_as_bytes(), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img








