from cv2 import cv2
import base64
import os
from .pupil_detect import detect_face_and_eye
from ..models import DiameterInfo


def generate_frame(file=None):
    video_cap = cv2.VideoCapture(file)
    # frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    cnt = 0
    success, image = video_cap.read()
    frame_list=[]
    # fps_in=video_cap.get(cv2.CAP_PROP_FPS)
    # print('fps before ', fps_in)
    # video_cap.set(cv2.CAP_PROP_FPS,20)
    # fps_in = video_cap.get(cv2.CAP_PROP_FPS)
    # print('fps after ', fps_in)
    while success:
        # _,frame=video_cap.read()
        frame=image
        frame_list.append(frame)
        # print(frame.shape)
        cnt+=1
        success, image = video_cap.read()
    # success, image = video_cap.read()

    # while success:
    #     cv2.imwrite("frame%d.jpg" % cnt, image)  # save frame as JPEG file
    #     success, image = video_cap.read()
    #     cnt+=1


    # print(frame_height)
    # print(frame_width)
    # print(fps)
    print('total frame generated : ',cnt)
    return frame_list


def convert_base_64(file):
    # with open(file, "rb") as videoFile:
    #     text = base64.b64encode(videoFile.read())
    #     print(text)
    #     # file = open("textTest.txt", "wb")
    #     # file.write(text)
    #     # file.close()
    #
    #     fh = open("video.mp4", "wb")
    #     fh.write(base64.b64decode(text))
    #     fh.close()
    if os.path.isfile("video.mp4"):
        os.remove("video.mp4")
    text=file
    # with open('/Users/laistesham/Downloads/video_base64.txt','rb') as f:
    #     text=f.read()
    fh = open("video.mp4", "wb")
    fh.write(base64.b64decode(text))
    fh.close()
        # need to test
        # base 64 video write to a temp video
        #  then read from that
    video_cap = cv2.VideoCapture("video.mp4")
    success, image = video_cap.read()
    cnt=0
    fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    frame_list = []
    while success:
        # _,frame=video_cap.read()
        frame=image
        # print(frame.shape)
        frame_list.append(frame)
        cnt+=1
        success, image = video_cap.read()
    print(cnt)
    return frame_list


def generate_frame_and_detect_pupil_diameter(data,model):
    files = data.get('files')
    age = data.get('age')
    gender = data.get('gender')
    participantIndex = data.get('participantIndex')
    # phoneBrand = data.get('phoneBrand') if data.get('phoneBrand') else ''
    # phoneModel = data.get('phoneModel') if data.get('phoneModel') else ''
    sleepTime = data.get('sleepTime')

    for item in files:
        file_path=item.get('file_path')
        video_cap = cv2.VideoCapture(file_path)
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))
        print('frame: ',fps)
        success, image = video_cap.read()
        while success:
            frame=image
            distance = item.get('distance')
            diameter=detect_face_and_eye(frame,model,distance=distance)
            # need to save data in the database
            file_name=item.get('name')
            rating=item.get('rating')
            verdict=item.get('verdict')

            pupil_info=DiameterInfo(
                file_name=file_name,
                file_path=file_path,
                age=age,
                rating=rating,
                verdict=verdict,
                diameter=diameter,
                gender=gender,
                participant_index=participantIndex,
                # phone_brand=phoneBrand,
                # phone_model=phoneModel,
                sleep_time=sleepTime,
                distance=distance
            )
            pupil_info.save()
            success, image = video_cap.read()



