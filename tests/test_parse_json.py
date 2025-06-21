if __name__ == "__main__":
        
    response = """```json
        {
            "responses": [
                {
                    "poem_number": 1,
                    "poem_text": "cởi trời xanh cởi đất nâu\n" +
                        "gió mây cũng đã bắc cầu sang nhau\n" +
                        "để cho tình có được màu\n" +
                        "không còn nhung nhớ mong cầu trời thư\n" +
                        "và em như thực như hư\n" +
                        "thư anh vừa gửi hay thư ông trời\n" +
                        "càn khôn như cũng thảnh thơi\n" +
                        "khi ta không giận không lời dối gian"
                },
                {
                    "poem_number": 2,
                    "poem_text": "cởi trời xanh cởi đất nâu\n" +
                        "gió mây cũng đã bắc cầu sang nhau\n" +
                        "để cho tình có được màu\n" +
                        "không còn nhung nhớ mong cầu trời hư\n" +
                        "và em như thực như hư\n" +
                        "thư anh vừa gửi hay thư ông trời\n" +
                        "càn khôn như cũng thảnh thơi\n" +
                        "khi ta không giận không lời dối gian"
                },
                {
                    "poem_number": 3,
                    "poem_text": "cởi trời xanh cởi đất nâu\n" +
                        "gió mây cũng đã bắc cầu sang nhau\n" +
                        "để cho tình có được màu\n" +
                        "không còn nhung nhớ mong cầu trời dư\n" +
                        "và em như thực như hư\n" +
                        "thư anh vừa gửi hay thư ông trời\n" +
                        "càn khôn như cũng thảnh thơi\n" +
                        "khi ta không giận không lời dối gian"
                },
                {
                    "poem_number": 4,
                    "poem_text": "cởi trời xanh cởi đất nâu\n" +
                        "gió mây cũng đã bắc cầu sang nhau\n" +
                        "để cho tình có được màu\n" +
                        "không còn nhung nhớ mau cầu trời thư\n" +
                        "và em như thực như hư\n" +
                        "thư anh vừa gửi hay thư ông trời\n" +
                        "càn khôn như cũng thảnh thơi\n" +
                        "khi ta không giận không lời dối gian"
                },
                {
                    "poem_number": 5,
                    "poem_text": "cởi trời xanh cởi đất nâu\n" +
                        "gió mây cũng đã bắc cầu sang nhau\n" +
                        "để cho tình có được màu\n" +
                        "không còn nhung nhớ mong cầu trời dâng\n" +
                        "và em như thực như hư\n" +
                        "thư anh vừa gửi hay thư ông trời\n" +
                        "càn khôn như cũng thảnh thơi\n" +
                        "khi ta không giận không lời dối gian"
                }
            ]
        }
        ```
    """
    response = """
    {
        "responses": [
            {
                "poem_number": 1,
                "poem_text": "bên thềm xuân mới với đào\n gió xuân nhẹ thổi ngạt ngào hương thơm\n nụ đào chúm chím mềm thơm\n hồng hồng đôi má tươi thơm mơ mây\n chờ anh em đợi mỗi chiều\n xuân về tết đến bao điều ước mong\n tình đầu sao cứ long đong\n bao giờ cho thỏa ước mong hai mình"
            },
            {
                "poem_number": 2,
                "poem_text": "bên thềm xuân mới với đào\n gió xuân nhẹ thổi ngạt ngào hương thơm\n nụ đào chúm chím lành thơm\n hồng hồng đôi má đong thơm say mây\n chờ anh em đợi mỗi chiều\n xuân về tết đến bao điều ước mong\n tình đầu sao cứ long đong\n bao giờ cho thỏa ước mong hai mình"
            },
            {
                "poem_number": 3,
                "poem_text": "bên thềm xuân mới với đào\n gió xuân nhẹ thổi ngạt ngào hương thơm\n nụ đào chúm chím ngọt thơm\n hồng hồng đôi má say thơm mượt mây\n chờ anh em đợi mỗi chiều\n xuân về tết đến bao điều ước mong\n tình đầu sao cứ long đong\n bao giờ cho thỏa ước mong hai mình"
            },
            {
                "poem_number": 4,
                "poem_text": "bên thềm xuân mới với đào\n gió xuân nhẹ thổi ngạt ngào hương thơm\n nụ đào chúm chím trong thơm\n hồng hồng đôi má hồng thơm mê mây\n chờ anh em đợi mỗi chiều\n xuân về tết đến bao điều ước mong\n tình đầu sao cứ long đong\n bao giờ cho thỏa ước mong hai mình"
            },
            {
                "poem_number": 5,
                "poem_text": "bên thềm xuân mới với đào\n gió xuân nhẹ thổi ngạt ngào hương thơm\n nụ đào chúm chím nhẹ thơm\n hồng hồng đôi má non thơm say mây\n chờ anh em đợi mỗi chiều\n xuân về tết đến bao điều ước mong\n tình đầu sao cứ long đong\n bao giờ cho thỏa ước mong hai mình"
            }
        ]
    }
    """

    import re
    import json

    if response.startswith("```"):
        match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
        if match:
            response = match.group(1).strip()
    def clean_json_string(bad_json):
        # Remove all `+` signs
        cleaned = re.sub(r'\s*\+\s*', '', bad_json)
        return cleaned
    response = clean_json_string(response)
    response = response.replace('""', '')
    # This regex will handle newlines inside the values
    response = re.sub(r'(?<=: ")(.*?)(?=")', lambda m: m.group(0).replace('\n', '\\n'), response, flags=re.DOTALL)

    # Replace
    print(response) 

    json_response = json.loads(response)
