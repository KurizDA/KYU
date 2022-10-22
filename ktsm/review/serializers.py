from rest_framework import serializers
from .models import VideoEmotionChartData, VideoQuestionData

class VideoEmotionChartDataSerializer(serializers.ModelSerializer) :
    class Meta :
        model = VideoEmotionChartData 
        fields = '__all__'   


class VideoQuestionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoQuestionData
        fields = '__all__'

