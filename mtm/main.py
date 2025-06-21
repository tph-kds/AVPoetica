import os 
import re
import time 
import json
import  pandas as pd
import numpy as np

from mtm.models import (
    DeepSeekModel, 
    OpenRouterModel
)
from mtm.processes import RhymesTonesMetrics
from mtm.configs.schemas import (
    DeepSeekModelConfig, 
    OpenRouterModelConfig,
    PoeticRulesConfig,
    CountSyllablePoemsConfig,
    MaskErrorTokenizationConfig,
    PoeticRulesMetricsConfig
)
from mtm.configs import *
from mtm.prompts import SYSTEM_PROMPT

from mtm.processes import MaskErrorTokenization
from mtm.utils import read_file_from_url

def create_prompt_user(user_prompt: str) -> str:
    prompt = f"""
    \n\n**My poem is:**\n{user_prompt}
    """
    return prompt


def read_datasets(
        path: str,
        column: str
) -> str:
    """
        A function to read dataset for evaluating the corrected poem input testing 
        
        Args:
            path (str): path of dataset file

        Returns:
            str: dataset
    """

    dataset = read_file_from_url(path)
    # Check if column exists
    if column not in dataset:
        raise ValueError(f"Column {column} not found in dataset")
    # Return all columns having as possible as input of dataset
    if column is None:
        return dataset
    # Return specific column
    return dataset[f"{column}"]


def calculate_top_k(
        poem_inputs: Dict[str, Any],
        metrics: RhymesTonesMetrics,
        all_responses: List[Dict[str, Any]],
        tag: str,
        k: int = 3,
):
    """
        A function to check and calculate top-k score of  generated poems from OpenRouterModel and DeepSeekModel

        Args:
            poem_inputs (Dict[str, Any]): poems generated from OpenRouterModel and DeepSeekModel
            metrics (RhymesTonesMetrics): rhymes and tones metrics
            tag (str): tag Input - type of poem
            k (int, optional): top-k. Defaults to 3.

        Returns:
            top_k: top-k score

    """
    outputs = {}
    poems = []
    scores = []
    for i, poem in enumerate(poem_inputs):
        score = metrics.calculate_score(
            poem=poem["poem_text"],
            tag=tag
        )
        poems.append(poem["poem_text"])
        scores.append(score)

        # Add response to all_responses
        poem_inputs[i]["score"] = score
    top_k = sorted(zip(poems, scores), key=lambda x: x[1], reverse=True)[:k]
    outputs["corrected_poem"] = top_k[0][0]
    outputs["corrected_score"] = top_k[0][1]
    outputs["top_k_corrected_score"] = np.mean(scores)

    # Add all responses to all_responses
    all_responses.append(poem_inputs)
    return outputs
        

if __name__ == "__main__":

    r_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n\n[ROOT_PATH]: {r_path} \n\n")

    data = read_datasets(
        path=GOOGLE_SHEETS_URL, 
        column="Qwen_output"
    )
    print(f"data: \n{data}")
    
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
    # Configuration for DeepSeek modeling 
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

    metrics_config =  PoeticRulesMetricsConfig(
        vowels_dict_path = VOWELS_DICT_PATH,
        rhyme_dict_path = RHYME_DICT_PATH,
        tone_dict_path = TONE_DICT_PATH,
        dictionary_path = DICTIONARY_PATH,
        special_tone_dict_path = SPECIAL_TONE_DICT_PATH
    )

    metrics = RhymesTonesMetrics(
        metrics_config = metrics_config
    )


    all_responses, poem_inputs, corrected_poems, prompt_inputs, top_k_poems, generated_times, corrected_scores, top_k_corrected_scores =  [[] for _ in range(8)]
    
    df = pd.DataFrame(
        columns=[
            "poem_input",
            "final_poem",
            "user_prompt",
            "top_k",
            "time",
            "corrected_score",
        ],
        index=None,
        dtype=str
    )


    #  Running all around the dataset for evaluating the model
    for i in range(len(data)):
        print(f"\n[MASK ERROR TOKENIZATION]: Begin processing stanza {i + 1}...")
        poem_input, luc_bat, final_poem = met.mask_error_tokenization(
            poem_input = data[i]
        )
        print(final_poem)
        print(f"\nCompleted MASK ERROR TOKENIZATION SUCCESSFULLY")
        tag = "68" if luc_bat else "78"

        user_prompt = create_prompt_user(user_prompt = final_poem)
        print(user_prompt)
        # Check score before calling reasoning model
        check_score = metrics.calculate_score(
            poem=poem_input,
            tag=tag
        )
        #  Calling Reasoning Model From OpenRouter Framework
        #  calculate time
        start_time = time.time()
        if check_score >= 100.0:
            json_response, recall_counts = {"responses": [{"poem_number": 1, "poem_text": poem_input}]}, 1
        else:
            print(f"[OPENROUTER MODEL]: Begin processing stanza ...")
            response, recall_counts = openrouter_model.calling_model(user_prompt=user_prompt)
            if response == None:
                json_response, recall_counts = {"responses": [{"poem_number": 1, "poem_text": poem_input}]}, -1
            print(f"json_response: \n{response}")
            
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

            try:
                json_response = json.loads(response)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON from response:", e)
            # json_response = json.loads(response)
        # End time
        end_time = time.time()
        print(f"Completed OPENROUTER MODEL SUCCESSFULLY")

        # Calculate range of runing time
        range_time = end_time - start_time

        print(f"[CACULATE TOP K]: Begin processing stanza ...")
        # Calculate the final poem which would be saved including 
        # all_response_poems : having both original and top k generated poems
        # corrected_poem : having only top 1 generated poems having highest corrected score
        # corrected_score : having only top 1 generated poems having highest corrected score
        results = calculate_top_k(
            poem_inputs=json_response["responses"],
            metrics=metrics,
            all_responses=all_responses,
            tag = tag,
            k=1
        )
        # final_poem = ""
        corrected_score = results["corrected_score"]
        corrected_poem = results["corrected_poem"]
        top_k_corrected_score = results["top_k_corrected_score"]

        
        # Save data to list storage
        # all_responses.extend(response["responses"])
        # poem_inputs.append(data[i])
        # generated_times.append(range_time)
        # corrected_poems.append(corrected_poem)
        # prompt_inputs.append(user_prompt)
        # top_k_poems.append(json_response["responses"])
        # corrected_scores.append(corrected_score)
        # top_k_corrected_scores.append(top_k_corrected_score)
        print(f"Completed CACULATE TOP K SUCCESSFULLY")
        print(f"RUNNING STANZA {i + 1} COMPLETED SUCCESSFULLY")

        print(f"poem_input: {data[i]}")
        print(f"final_poem: {corrected_poem}")
        print(f"user_prompt: {user_prompt}")
        print(f"top_k: {json_response['responses']}")
        print(f"time: {range_time}")
        print(f"corrected_score: {corrected_score}")
        print(f"corrected_score_topk: {top_k_corrected_score}")


        # print(f"Resetting request rate and calling the model after {i + 1} stanzas... Sleeping for 60 seconds...")

        # Build DataFrame directly from data
        df_extened = pd.DataFrame({
            "poem_input": [data[i]],
            "final_poem": [corrected_poem],
            "user_prompt": [user_prompt],
            "top_k": [str(json_response["responses"])],
            "time": [range_time],
            "corrected_score": [corrected_score],
            "corrected_score_topk": [top_k_corrected_score],
            "recall_counts": [recall_counts],
        },
            index=None,
            dtype=str
        )

        # Append to CSV
        df_path = os.path.join(r_path, "result.csv")
        if not os.path.exists(df_path):
            df_extened.to_csv(df_path, mode="w", index=False)
        elif os.path.getsize(df_path) == 0:
            df_extened.to_csv(df_path, mode="w", header=True, index=False) 
        else:
            df_extened.to_csv(df_path, mode="a", header=not os.path.exists(df_path), index=False)
        print(f"Saved to CSV: {df_path} at stanza {i + 1}")

        # Handle JSON
        json_data_path = os.path.join(r_path, "all_responses.json")
        print(f"Saving result to JSON: {json_data_path}  at stanza {i + 1}")
        if os.path.exists(json_data_path):
            with open(json_data_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content == "":
                    existing_data = []
                else:
                    existing_data = json.loads(content)
        else:
            existing_data = []

        existing_data.extend(all_responses)

        with open(json_data_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)


        if i % 5 == 0:
            print(f"Sleeping for 60 seconds... at stanza {i + 1}")
            time.sleep(60)
    # print(f"\nBeginning saving result to csv file at {os.getcwd()}/result.csv\n")

    # #  Save csv file 
    # df["poem_input"] = poem_inputs
    # df["final_poem"] = corrected_poems
    # df["user_prompt"] = prompt_inputs
    # df["top_k"] = top_k_poems
    # df["time"] = generated_times
    # df["corrected_score"] = corrected_scores
    # df["corrected_score_topk"] = top_k_corrected_scores

    # print(f"poem_inputs: \n{poem_inputs}\n")
    # print(f"final_poems: \n{corrected_poems}\n")
    # print(f"prompt_inputs: \n{prompt_inputs}\n")
    # print(f"top_k_poems: \n{top_k_poems}\n")
    # print(f"generated_times: \n{generated_times}\n")
    # print(f"corrected_scores: \n{corrected_scores}\n")
    # print(f"top_k_corrected_scores: \n{top_k_corrected_scores}\n")
    # df.to_csv("result.csv", index=False)


    # print(f"Implemented saving result to csv file at {os.getcwd()}/result.csv\n")

    # # Save json file for all responses
    # print(f"Beginning saving result to json file at {os.getcwd()}/all_responses.json\n")
    # with open("all_responses.json", "w", encoding="utf-8") as f:
    #     json.dump(all_responses, f, ensure_ascii=False, indent=4)

    # print(f"Implemented saving result to json file at {os.getcwd()}/all_responses.json\n")



    # poem_input = "hạ long thắng cảnh nên màu \nnúi non nước gợn sống vỗ về đâu \ntrời mây xanh thẳm yên bình \ncây reo gió hát bóng nhẹ nhàng trôi"

    # mask_err_tok_config = MaskErrorTokenizationConfig(
    #     poetic_config = PoeticRulesConfig(
    #         vowels_dict_path = VOWELS_DICT_PATH,
    #         rhyme_dict_path = RHYME_DICT_PATH,
    #         tone_dict_path = TONE_DICT_PATH,
    #         dictionary_path = DICTIONARY_PATH,
    #         special_tone_dict_path = SPECIAL_TONE_DICT_PATH
    #     ),
    #     count_syllable_config = CountSyllablePoemsConfig(
    #         masked_words = CS_MASKED_WORDS,
    #         idx_masked_words = CS_IDX_MASKED_WORDS,
    #         token_masked_words = CS_TOKEN_MASKED_WORDS
    #     )
    # )

    # met = MaskErrorTokenization(
    #     met_config = mask_err_tok_config
    # )
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

    # poem_input = "Hoàng hôn tắt nắng phủ sương \nbóng tối giăng đầy vạn nẻo mơ mờ \nngọn cỏ thu sương lay khẽ khẽ \nđầu non điểm xuyết ánh lơ thơ \ncôn trùng rỉ rả nghe mà chán \ncon nhên buông tơ rối cả trơ \nlặng lẽ tìm con buồn héo hắt \nkhói sương lẩn khuât không một ai."
    # poem_input, final_poem = met.mask_error_tokenization(
    #     poem_input = poem_input
    # )
    # print(final_poem)
    # user_prompt = create_prompt_user(user_prompt = final_poem)
    # print(user_prompt)
    # user_prompt_test_2 = """
    # \n\n**My poem is:** 
    # \nHoàng hôn tắt nắng phủ sương mờ (7_1)
    # \nbóng tối giăng đầy vạn nẻo mơ (7_2)
    # \nngọn cỏ thu sương lay khẽ khẽ (7_3)
    # \nđầu non điểm xuyết ánh lơ thơ (7_4)
    # \ncôn trùng rỉ rả nghe mà chán (7_5)
    # \ncon nhện buông tơ rối cả trơ (7_6)
    # \nlặng lẽ tìm con buồn héo hắt (7_7)
    # \nkhói sương lẩn khuất [MASKED_WORD] [MASKED_WORD] [MASKED_WORD] (7_8)
    # """

    # print(user_prompt_test_2)
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