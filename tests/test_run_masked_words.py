from mtm.mtm.processes import MaskErrorTokenization
from mtm.mtm.configs import *


if __name__ == "__main__":

    # Configuration for MaskErrorTokenization Function 
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

    poem_input = "con xin một trái nha ông \n nhà còn ít nhưng không muốn thừa \nnhìn ông lúc nắng lúc mưa \nđi đâu bà cũng sớm trưa bên mình \nmột thời vất vả mưu sinh \nnh℉ vui có bóng hình bên ta \ngiờ đây tóc bạc trắng ngà \nbà đi để lại căn nhà vắng tanh"
    poem_input_1 = "thơ đề ba bức mực chưa phai \nmột gánh giang sơn một gánh sầu \ntấc dạ nhớ quê lòng lại nhớ \nnon sông cách trở biển thêm sầu \nhồn quê chen chúc hồn thiên quốc \ntiếng quạ vang rền tiếng chiến binh \nđỉnh ngự còn ca lời dặn \nlòng ai thay đá chẳng phai màu"
    poem_input_2 = "tuổi thơ từ trải bước sang hèn \nđã thấy xuân về với gió men \nchén rượu nhớ hoài ngày tháng cũ \ncây mai xao xuyến節 năm ngoen \nđường xưa lá mới  lưa thưa rải \nbến cũ đêm nay vắng vẻ đèn \nsương giá không còn trên mái tóc \nhồ thu hương lửa mới lên men"
    poem_input_3 = "con xin một trái nha ông \ncủa nhà còn ít nhưng không muốn thừa \nnhìn ông lúc nắng lúc mưa \nđi đâu bà cũng sớm trưa bên mình \nmột thời vất vả mưu sinh \nnh℉ vui có bóng hình bên ta \ngiờ đây tóc bạc trắng ngà \nbà đi để lại căn nhà vắng tanh"
    
    # poem_input = met._check_error_vietnamese_words(poem_input = poem_input)
    # print(f"Checking error Vietnamese words: \n{poem_input}")
    poem_input, luc_bat, final_poem = met.mask_error_tokenization(poem_input_3)

    print(f"poem_input: \n{poem_input}")
    print(f"luc_bat: {luc_bat}")
    print(f"final_poem: \n{final_poem}")

