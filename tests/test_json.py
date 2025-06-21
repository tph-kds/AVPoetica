
if __name__ == "__main__":
    import os
    import json

    r_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_data_path = os.path.join(r_path, "all_responses.json")
    if os.path.exists(json_data_path):
        with open(json_data_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if content == "":
                existing_data = []
            else:
                existing_data = json.loads(content)
    else:
        existing_data = []
    all_responses = [
        {
            "poem_number": 4,
            "poem_text": "cởi trời xanh cởi đất nâu\ngió mây cũng đã bắc cầu sang nhau\nđể cho tình có được màu\nkhông còn nhung nhớ nỗi sầu trong thư\nvà em như thực như hư\nthư anh vừa gửi hay thư ông trời\ncàn khôn như cũng thảnh thơi\nkhi ta không giận không lời dối gian",
            "score": 93.63636363636364
        },
        {
            "poem_number": 5,
            "poem_text": "cởi trời xanh cởi đất nâu\ngió mây cũng đã bắc cầu sang nhau\nđể cho tình có được màu\nkhông còn nhung nhớ đắng cay sầu từ\nvà em như thực như hư\nthư anh vừa gửi hay thư ông trời\ncàn khôn như cũng thảnh thơi\nkhi ta không giận không lời dối gian",
            "score": 93.63636363636364
        }
    ]
    existing_data.extend(all_responses)

    with open(json_data_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
    
    print(f"existing_data: {existing_data}")