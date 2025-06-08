from mtm.models import DeepSeekModel
from mtm.configs.schemas import DeepSeekModelConfig
from mtm.configs import *
from mtm.prompts import SYSTEM_PROMPT

if __name__ == "__main__":
    user_prompt = """
    **My poem is:** 
       hạ long thắng cảnh nên [MASKED_WORD] (6_1) 
       núi non nước gợn sóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_1)      
       trời mây xanh thẳm yên bình  (6_2) 
       cây reo gió hát bóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_2)
    """
    user_prompt_2 = """
    **My poem is:** 
    Hoàng hôn tắt nắng phủ sương mờ (7_1)
    bóng tối giăng đầy vạn nẻo mơ (7_2)
    ngọn cỏ thu sương lay khẽ khẽ (7_3)
    đầu non điểm xuyết ánh lơ thơ (7_4)
    côn trùng rỉ rả nghe mà chán (7_5)
    con nhện buông tơ rối cả trơ (7_6)
    lặng lẽ tìm con buồn héo hắt (7_7)
    khói sương lẩn khuất [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (7_8)
    """
    deepseek_model = DeepSeekModel(
        model_config=DeepSeekModelConfig(
            SYSTEM_PROMPT=SYSTEM_PROMPT,
            DEEPSSEEK_MODEL_NAME=DEEPSEEK_MODEL_NAME,
            DEEPSEEK_API_KEY=DEEPSEEK_API_KEY,
            BASE_URL=BASE_URL,
            STREAM=STREAM,
            TEMPERATURE=TEMPERATURE,
            MAX_TOKENS=MAX_TOKENS,
        ))
    response = deepseek_model.calling_deepseek(user_prompt=user_prompt)
    print(response)


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