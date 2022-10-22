from django.shortcuts import render
from rest_framework.response import Response
from .models import VideoEmotionChartData, VideoQuestionData
from rest_framework.views import APIView
from .serializers import VideoEmotionChartDataSerializer, VideoQuestionDataSerializer
from . import chat_json_maker
from . import time_pos_neg

class VideoEmotionChartDataListAPI(APIView):
    def get(self, request, request_video_id):
        queryset = VideoEmotionChartData.objects.filter(video_id=request_video_id)
        print(queryset)
        serializer = VideoEmotionChartDataSerializer(queryset, many=True)
        return Response(serializer.data)

class VideoQuestionDataListAPI(APIView):
    def get(self, request, request_video_id):
        queryset = VideoQuestionData.objects.filter(video_id=request_video_id)
        print(queryset)
        serializer = VideoQuestionDataSerializer(queryset, many=True)
        return Response(serializer.data)

class VideoDataMaker():
    def makeData(request, request_video_id):
        chat_json_maker.make_json(request_video_id)
        time_pos_neg.json_file_insert(request_video_id)
        VideoEmotionChartDataListAPI.as_view()

