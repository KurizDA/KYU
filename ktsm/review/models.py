from django.db import models

class VideoEmotionChartData(models.Model):
    video_id = models.IntegerField()
    review_time = models.CharField(max_length=10)
    positive_chat_count = models.IntegerField()
    neturality_chat_count = models.IntegerField()
    negative_chat_count = models.IntegerField()
    question_chat_count = models.IntegerField()
    total_chat_count = models.IntegerField()

    def __str__(self):
        return self.review_time

class VideoQuestionData(models.Model):
    video_id = models.IntegerField()
    chat_time = models.CharField(max_length=20)
    chat_name = models.CharField(max_length=30)
    chat_comment = models.CharField(max_length=100)
