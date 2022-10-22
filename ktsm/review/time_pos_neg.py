from . import load_model
import json

def json_file_insert(request_video_id):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ktsm.settings")
    import django
    django.setup()
    from .models import VideoEmotionChartData

    url = request_video_id + ".json"
    data = []
    data.append({"name": "00:00", "positive": 0, "nagative": 0, "question": 0, "neutrality": 0, "total": 0})
    VideoEmotionChartData(
                video_id = request_video_id,
                review_time = "00:00",
                positive_chat_count = 0,
                neturality_chat_count = 0,
                negative_chat_count = 0,
                question_chat_count = 0,
                total_chat_count = 0,
            ).save()

    with open(url, 'r', encoding = "UTF-8") as f:
        json_data = json.load(f)
        k = total = _pos = _neg = _neu = _qus = 0
        pos = neg = neu = qus = 0
        for i in range(len(json_data)):
            if (json_data[i]["min"]//60) <= k:
                _, emotion = load_model.live_chat(json_data[i]["message"])
                if emotion == "부정": neg += 1
                elif emotion == "긍정": pos += 1
                elif emotion == "질문": qus += 1
                else: neu += 1
                _pos = pos
                _neg = neg
                _neu = neu
                _qus = qus
            else:
                total += pos + neg + qus + neu
                data.append({"name": "{:02}:00".format(k+1), "postive": _pos, "negative": _neg, "question": _qus, "neutrality": _neu, "total": total})
                VideoEmotionChartData(
                            video_id = request_video_id,
                            review_time = "{:02}:00".format(k+1),
                            positive_chat_count = _pos,
                            neturality_chat_count = _neu,
                            negative_chat_count = _neg,
                            question_chat_count = _qus,
                            total_chat_count = total,
                        ).save()

                k += 1
                i -= 1
                pos = neg = neu = qus = 0
        total += pos + neg + qus + neu
        data.append({"name": "{:02}:00".format(k+1), "postive": _pos, "negative": _neg, "question": _qus, "neutrality": _neu, "total": total})
        VideoEmotionChartData(
                    video_id = request_video_id,
                    review_time = "{:02}:00".format(k+1),
                    positive_chat_count = _pos,
                    neturality_chat_count = _neu,
                    negative_chat_count = _neg,
                    question_chat_count = _qus,
                    total_chat_count = total,
                ).save()
    f.close()

    print(json.dumps(data, indent="\t") )
