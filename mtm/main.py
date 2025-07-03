import os 
import re
import time 
import json
import  pandas as pd
import numpy as np

from .mtm.models import (
    DeepSeekModel, 
    OpenRouterModel
)
from .mtm.processes import RhymesTonesMetrics
from .mtm.configs.schemas import (
    DeepSeekModelConfig, 
    OpenRouterModelConfig,
    PoeticRulesConfig,
    CountSyllablePoemsConfig,
    MaskErrorTokenizationConfig,
    PoeticRulesMetricsConfig
)
from .mtm.configs import *
from .mtm.prompts import SYSTEM_PROMPT

from .mtm.processes import MaskErrorTokenization
from .mtm.utils import read_file_from_url

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

    return outputs
        

def mtm_main(
        generated_poem: str,
):
    """
        Main function to run the Masked Tokenization Model (MTM) for evaluating the poem input
    """
    print(f" ******************* STARTING MTM MAIN FUNCTION ... *******************\n\n")
    # # Load environment variables
    # r_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(f"\n\n[ROOT_PATH]: {r_path} \n\n")
    
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




    print(f"\n[MASK ERROR TOKENIZATION]: Begin processing stanza...")
    poem_input, luc_bat, final_poem = met.mask_error_tokenization(
        poem_input = generated_poem
    )
    # print(final_poem)
    print(f"\nCompleted MASK ERROR TOKENIZATION SUCCESSFULLY")
    tag = "68" if luc_bat else "78"

    user_prompt = create_prompt_user(user_prompt = final_poem)
    # print(user_prompt)
    # Check score before calling reasoning model
    check_score = metrics.calculate_score(
        poem=poem_input,
        tag=tag
    )

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

    print(f"Completed OPENROUTER MODEL SUCCESSFULLY")

    print(f"[CACULATE TOP K]: Begin processing stanza ...")
    results = calculate_top_k(
        poem_inputs=json_response["responses"],
        metrics=metrics,
        tag = tag,
        k=1
    )
    print(f"******************* Completed MTM SMALL FUNCTION SUCCESSFULLY ***************************\n\n")

    return results["corrected_poem"]


