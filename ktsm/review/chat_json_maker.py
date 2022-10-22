import twitch
import json
# from collections import OrderedDict

def make_json(request_video_id):
    video_ID = request_video_id
    helix = twitch.Helix('y4rg1nyysvc09kqxx9e7pqx56br2h4', 'rlodb4xw8v29m0wvtt1taeodgtyyzp')
    test_video = helix.video(video_ID)

    start_time = test_video.created_at
    start_hour = int(start_time[11:13])
    start_min = int(start_time[14:16])
    start_sec = int(start_time[17:19])
    start_msec = 0

    json_dict = []

    temp = 0
    for comment in test_video.comments:
        chat_time = comment.created_at
        chat_hour = int(chat_time[11:13])
        chat_min = int(chat_time[14:16])
        chat_sec = int(chat_time[17:19])
        chat_msec = chat_time[19:]
        if chat_msec[0] == 'Z':
            chat_msec = 0
        else:
            chat_msec = int(chat_msec[1:len(chat_msec)-1])
        after_sec = chat_sec-start_sec
        if after_sec < 0:
            after_sec = after_sec + 60
            chat_min = chat_min - 1
        after_min = chat_min-start_min
        if after_min < 0:
            after_min = after_min + 60
            chat_hour = chat_hour - 1
        after_hour = chat_hour-start_hour
        if after_hour < 0:
            after_hour = after_hour + 24

        temp = temp + 1
        if temp == 1:
            continue

        # row = [{ 'commenter_id': comment.commenter.id, 'display_name': comment.commenter.display_name, 'min': (after_hour*60)+after_min, 'sec': after_sec, 'msec': chat_msec, 'message' : comment.message.body }]
        row = [{'min': (after_hour*60)+after_min, 'message' : comment.message.body }]

        json_dict.extend(row)
        print(row)

    with open(video_ID + '.json', 'w', encoding='UTF-8') as outfile:
        json.dump(json_dict, outfile, ensure_ascii=False, indent="\t")
