import os 
from mtm.models import (
    DeepSeekModel, 
    OpenRouterModel
)
from mtm.configs.schemas import (
    DeepSeekModelConfig, 
    OpenRouterModelConfig,
    PoeticRulesConfig,
    CountSyllablePoemsConfig,
    MaskErrorTokenizationConfig
)
from mtm.configs import *
from mtm.prompts import SYSTEM_PROMPT

from mtm.processes import MaskErrorTokenization

def create_prompt_user(user_prompt: str) -> str:
    prompt = f"""
    \n\n**My poem is:**\n{user_prompt}
    """
    return prompt

if __name__ == "__main__":
    poem_input = "hạ long thắng cảnh nên màu \nnúi non nước gợn sống vỗ về đâu \ntrời mây xanh thẳm yên bình \ncây reo gió hát bóng nhẹ nhàng trôi"

    mask_err_tok_config = MaskErrorTokenizationConfig(
        poetic_config = PoeticRulesConfig(
            vowels_dict_path = VOWELS_DICT_PATH,
            rhyme_dict_path = RHYME_DICT_PATH,
            tone_dict_path = TONE_DICT_PATH,
            dictionary_path = DICTIONARY_PATH,
            special_tone_dict_path = SPECIAL_TONE_DICT_PATH
        ),
        count_syllable_config = CountSyllablePoemsConfig(
            masked_words = CS_MASKED_WORDS,
            idx_masked_words = CS_IDX_MASKED_WORDS,
            token_masked_words = CS_TOKEN_MASKED_WORDS
        )
    )

    met = MaskErrorTokenization(
        met_config = mask_err_tok_config
    )
    # poem_input, final_poem = met.mask_error_tokenization(
    #     poem_input = poem_input
    # )
    # print(final_poem)
    # user_prompt = create_prompt_user(user_prompt = final_poem)
    # print(user_prompt)
    # user_prompt_test = """
    # \n\n**My poem is:** 
    #    \nhạ long thắng cảnh nên [MASKED_WORD] (6_1) 
    #    \nnúi non nước gợn sóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_1)      
    #    \ntrời mây xanh thẳm yên bình  (6_2) 
    #    \ncây reo gió hát bóng [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (8_2)
    # """
    # print(user_prompt_test)

    poem_input = "Hoàng hôn tắt nắng phủ sương \nbóng tối giăng đầy vạn nẻo mơ mờ \nngọn cỏ thu sương lay khẽ khẽ \nđầu non điểm xuyết ánh lơ thơ \ncôn trùng rỉ rả nghe mà chán \ncon nhên buông tơ rối cả trơ \nlặng lẽ tìm con buồn héo hắt \nkhói sương lẩn khuât không một ai."
    poem_input, final_poem = met.mask_error_tokenization(
        poem_input = poem_input
    )
    print(final_poem)
    user_prompt = create_prompt_user(user_prompt = final_poem)
    print(user_prompt)
    user_prompt_test_2 = """
    \n\n**My poem is:** 
    \nHoàng hôn tắt nắng phủ sương mờ (7_1)
    \nbóng tối giăng đầy vạn nẻo mơ (7_2)
    \nngọn cỏ thu sương lay khẽ khẽ (7_3)
    \nđầu non điểm xuyết ánh lơ thơ (7_4)
    \ncôn trùng rỉ rả nghe mà chán (7_5)
    \ncon nhện buông tơ rối cả trơ (7_6)
    \nlặng lẽ tìm con buồn héo hắt (7_7)
    \nkhói sương lẩn khuất [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (7_8)
    """

    print(user_prompt_test_2)
    # #  Calling Reasoning Model From OpenRouter Framework
    # import time
    # #  calculate time
    # start_time = time.time()

    # openrouter_model = OpenRouterModel(
    #     model_config=OpenRouterModelConfig(
    #         SYSTEM_PROMPT=SYSTEM_PROMPT,
    #         OPENROUTER_MODEL_NAME=OPENROUTER_MODEL_NAME,
    #         OPENROUTER_API_KEY=OPENROUTER_DEEPSEEK_API_KEY,
    #         OPENROUTER_BASE_URL=OPENROUTER_BASE_URL,
    #         STREAM=STREAM,
    #         TEMPERATURE=TEMPERATURE,
    #         MAX_TOKENS=MAX_TOKENS,
    #         RANKING_URL=RANKING_URL,
    #         RANKING_NAME=RANKING_NAME,
    #         INCLUDE_REASONING=INCLUDE_REASONING
    #     ))
    # response = openrouter_model.calling_model(user_prompt=user_prompt_2)
    # # End time
    # end_time = time.time()
    # range_time = end_time - start_time
    # #  Save json file
    # print(response)
    # print(f"Time to process: {range_time}")
    # import json 
    # with open("response.json", "w") as outfile:
    #     json.dump(response, outfile)
    #     print(f"Completed save file: response.json")


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