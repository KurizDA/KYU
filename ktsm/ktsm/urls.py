from django.contrib import admin
from django.urls import path
from review.views import VideoEmotionChartDataListAPI, VideoQuestionDataListAPI, VideoDataMaker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/<int:request_video_id>/makedata/', VideoDataMaker.makeData),
    path('review/<int:request_video_id>/emotionchartdata/', VideoEmotionChartDataListAPI.as_view()),
    path('review/<int:request_video_id>/questiondata/', VideoQuestionDataListAPI.as_view())
]
