import torch
from transformers import AutoTokenizer
import json

model = torch.load('model.pt')
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained("beomi/KcELECTRA-base")
LABELS = ["부정", "긍정", "질문", "없음"]
############################################
# 평가
def sentence_predict(sent):
    model.eval()

    # 입력된 문장 토크나이징
    tokenized_sent = tokenizer(
        sent,
        return_tensors="pt",
        truncation=True,
        add_special_tokens=True,
        max_length=128
    )
    
    # 모델이 위치한 GPU로 이동 
    tokenized_sent.to(device)

    # 예측
    with torch.no_grad():
        outputs = model(
            input_ids=tokenized_sent["input_ids"],
            attention_mask=tokenized_sent["attention_mask"],
            token_type_ids=tokenized_sent["token_type_ids"]
            )

    # 결과 return
    logits = outputs[0]
    logits = logits.detach().cpu()
    result = logits.argmax(-1)

    return result

##############################

#url = "./chatdata/chat_data_dduckhodduck.json"
#json_file_insert(url)

# 입력된 json파일을 전처리하고 predict함수로 보냄
def json_file_insert(request_video_id):
    url = request_video_id+'.json'
    with open(url, 'r', encoding = 'UTF-8') as f:
        json_data = json.load(f)

        chat = []
        for i in range(len(json_data)):
            chat.append(json_data[i]['message'])

        f.flush()
        f.close()

    predict_chat = predict(chat)
    emotion_rate(predict_chat, url)

# 채팅을 예측하고, 해당하는 레이블의 인덱스 반환
def predict(chat):
    chat_emotion = []
    
    for i in range(len(chat)):
        preds = sentence_predict(chat[i])
        array = preds.tolist()
        # 해당 array에서의 최대값을 찾은 후 해당 최대값에 해당하는 인덱스의 LABELS를 반환
        chat_emotion.append(LABELS[(array[0])])

    return chat_emotion

# 나온 덧글 감정에 따라 부정, 긍정, 중립으로 나누고, 비율을 출력
def emotion_rate(predict_chat, url):
    neg_rate = pos_rate = neu_rate = qus_rate = 0

    for i in range(len(predict_chat)):
        if predict_chat[i] == "부정": neg_rate += 1
        elif predict_chat[i] == "긍정": pos_rate += 1
        elif predict_chat[i] == "질문": qus_rate += 1
        else: neu_rate += 1

    print(neg_rate, pos_rate, qus_rate, neu_rate)

# 실시간 채팅 분석
def live_chat(chat):
    array = sentence_predict(chat).tolist()
    return chat, LABELS[array[0]]

if __name__=="__main__":
    main()


# 10 71 26 140
