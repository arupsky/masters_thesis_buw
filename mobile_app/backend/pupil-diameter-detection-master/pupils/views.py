# from django.shortcuts import render
from .response import  CoreResponse
from rest_framework.views import APIView
from pupils.ai_utils import pupil_detect, MTCNNFaceDetector
from keras import backend as K
import tensorflow as tf
from pupils.ai_utils import generate_frame,convert_base_64,generate_frame_and_detect_pupil_diameter
# from django.core.cache import cache
# Create your views here.
# session = K.get_session()
# with session.as_default():
#     with session.graph.as_default():
#         fd = MTCNNFaceDetector(sess=session, model_path=pupil_detect.mtcnn_weights_dir)
# print('dsaa',fd)
from .serializers import PupilRequestSerializer


class PupilDiameterApi(APIView):

    def post(self,request):

        try:
            tf.compat.v1.reset_default_graph()
            # fd_cache = cache.get('fd')
            # if not fd_cache:
            #     fd = MTCNNFaceDetector(sess=K.get_session(), model_path=pupil_detect.mtcnn_weights_dir)
            #     cache.set('fd','asd')
            #     fd_cache = fd
            img_urls = request.data.get('image_urls')
            sum_diameter = 0
            img_urls_length = len(img_urls)
            session = K.get_session()
            # with session.as_default():
            #     with session.graph.as_default():
            #         fd = MTCNNFaceDetector(sess=session, model_path=pupil_detect.mtcnn_weights_dir)
            fd = MTCNNFaceDetector(sess=session, model_path=pupil_detect.mtcnn_weights_dir)
            for img_url in img_urls:
                diameter = 0
                img = pupil_detect.get_image_from_firebase(img_url)
                if len(img)>0:
                    diameter = pupil_detect.detect_face_and_eye(img,fd)
                if diameter==0:
                    img_urls_length-=1
                sum_diameter = sum_diameter+diameter

            avg_diameter = sum_diameter/img_urls_length
            return CoreResponse.send(
                dict(
                    is_error=0,
                    message='success',
                    diameter=avg_diameter
                ), 200
            )
        except Exception as exc:
            return CoreResponse.send(
                dict(
                    is_error=1,
                    message=str(exc)
                ), 500
            )


class Test(APIView):
    def post(self,request):
        try:
            tf.compat.v1.reset_default_graph()
            # a=request.query_params.get('my_file')
            # a=request.data
            # dd=dict(request.data.lists())
            # d=dd['video_files']
            # ddd=a.get('video_files')['0']
            # dd=request.data['video_files'][1]
            video_files = dict(request.data.lists())['my_file']
            base64=request.data['base64']
            temp_path1 = video_files[0].temporary_file_path()
            # convert_base_64(temp_path1)
            # video=video_files[0]
            # vf=open(p,'rb')

            sum_diameter = 0
            avg_diameter = 0
            avg_diameter_list=[]
            # img_urls_length = len(frame_list)
            img_urls_length = 0
            session = K.get_session()
            fd = MTCNNFaceDetector(sess=session, model_path=pupil_detect.mtcnn_weights_dir)
            for video in video_files:
                temp_path = video.temporary_file_path()
                # frame_list = generate_frame(file=temp_path)
                frame_list=convert_base_64(base64)
                img_urls_length = len(frame_list)
                temp_sum_diameter=0
                temp_avg_diameter=0
                for frame in frame_list:
                    diameter = 0
                    diameter = pupil_detect.detect_face_and_eye(frame,fd)
                    if diameter==0:
                        img_urls_length-=1
                    temp_sum_diameter = temp_sum_diameter+diameter
                if img_urls_length!=0:
                    temp_avg_diameter = temp_sum_diameter/img_urls_length
                avg_diameter_list.append(temp_avg_diameter)
            return CoreResponse.send(
                dict(
                    is_error=0,
                    message='success',
                    diameter=avg_diameter_list
                ), 200
            )
        except Exception as exc:
            return CoreResponse.send(
                dict(
                    is_error=1,
                    message=str(exc)
                ), 500
            )



class PupilDiameterUpdatedApi(APIView):

    def post(self,request):

        try:
            tf.compat.v1.reset_default_graph()
            serializer = PupilRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            session = K.get_session()
            fd = MTCNNFaceDetector(sess=session, model_path=pupil_detect.mtcnn_weights_dir)
            generate_frame_and_detect_pupil_diameter(data=serializer.validated_data,model=fd)

            return CoreResponse.send(
                dict(
                    is_error=0,
                    message='success'
                ), 200
            )

        except Exception as exc:
            return CoreResponse.send(
                dict(
                    is_error=1,
                    message=str(exc)
                ), 500
            )