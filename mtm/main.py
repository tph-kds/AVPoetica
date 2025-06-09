from mtm.models import (
    DeepSeekModel, 
    OpenRouterModel
)
from mtm.configs.schemas import (
    DeepSeekModelConfig, 
    OpenRouterModelConfig
)
from mtm.configs import *
from mtm.prompts import SYSTEM_PROMPT

if __name__ == "__main__":
    user_prompt = """
    \n\n**My poem is:** 
       \nhạ long thắng cảnh nên [MASKED_WORD] (6_1) 
       \nnúi non nước gợn sóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_1)      
       \ntrời mây xanh thẳm yên bình  (6_2) 
       \ncây reo gió hát bóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_2)
    """
    user_prompt_2 = """
    \n\n**My poem is:** 
    \nHoàng hôn tắt nắng phủ sương [MASKED_WORD] (7_1)
    \nbóng tối giăng đầy vạn nẻo mơ (7_2)
    \nngọn cỏ thu sương lay khẽ khẽ (7_3)
    \nđầu non điểm xuyết ánh lơ thơ (7_4)
    \ncôn trùng rỉ rả nghe mà chán (7_5)
    \ncon nhện buông tơ rối cả [MASKED_WORD] (7_6)
    \nlặng lẽ tìm con buồn héo hắt (7_7)
    \nkhói sương lẩn khuất [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (7_8)
    """
    # deepseek_model = DeepSeekModel(
    #     model_config=DeepSeekModelConfig(
    #         SYSTEM_PROMPT=SYSTEM_PROMPT,
    #         DEEPSSEEK_MODEL_NAME=DEEPSEEK_MODEL_NAME,
    #         DEEPSEEK_API_KEY=DEEPSEEK_API_KEY,
    #         BASE_URL=BASE_URL,
    #         STREAM=STREAM,
    #         TEMPERATURE=TEMPERATURE,
    #         MAX_TOKENS=MAX_TOKENS,
    #     ))
    # response = deepseek_model.calling_deepseek(user_prompt=user_prompt)

    import time
    #  calculate time
    start_time = time.time()

    openrouter_model = OpenRouterModel(
        model_config=OpenRouterModelConfig(
            SYSTEM_PROMPT=SYSTEM_PROMPT,
            OPENROUTER_MODEL_NAME=OPENROUTER_MODEL_NAME,
            OPENROUTER_API_KEY=OPENROUTER_DEEPSEEK_API_KEY,
            OPENROUTER_BASE_URL=OPENROUTER_BASE_URL,
            STREAM=STREAM,
            TEMPERATURE=TEMPERATURE,
            MAX_TOKENS=MAX_TOKENS,
            RANKING_URL=RANKING_URL,
            RANKING_NAME=RANKING_NAME,
            INCLUDE_REASONING=INCLUDE_REASONING
        ))
    response = openrouter_model.calling_model(user_prompt=user_prompt_2)
    # End time
    end_time = time.time()
    range_time = end_time - start_time
    #  Save json file
    print(response)
    print(f"Time to process: {range_time}")
    import json 
    with open("response.json", "w") as outfile:
        json.dump(response, outfile)
        print(f"Completed save file: response.json")


    # python mtm/main.py


# Output Example:
# {
#   "responses": [
#     {
#       "poem_number": 1,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất bóng con thơ"
#     },
#     {
#       "poem_number": 2,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất dáng con thơ"
#     },
#     {
#       "poem_number": 3,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất hình con thơ"
#     },
#     {
#       "poem_number": 4,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất nơi con thơ"
#     },
#     {
#       "poem_number": 5,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất bé con thơ"
#     },
#     {
#       "poem_number": 6,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất bóng hình thơ"
#     },
#     {
#       "poem_number": 7,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất nỗi buồn thơ"
#     },
#     {
#       "poem_number": 8,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất chốn con thơ"
#     },
#     {
#       "poem_number": 9,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất cõi mộng thơ"
#     },
#     {
#       "poem_number": 10,
#       "poem_text": "Hoàng hôn tắt nắng phủ sương mờ
#       \nbóng tối giăng đầy vạn nẻo mơ
#       \nngọn cỏ thu sương lay khẽ khẽ
#       \nđầu non điểm xuyết ánh lơ thơ
#       \ncôn trùng rỉ rả nghe mà chán
#       \ncon nhện buông tơ rối cả trơ
#       \nlặng lẽ tìm con buồn héo hắt
#       \nkhói sương lẩn khuất lối vào thơ"
#     }
#   ]
# }