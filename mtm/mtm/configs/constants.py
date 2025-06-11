import os 

BASE_URL="https://api.deepseek.com"
DEEPSEEK_MODEL_NAME = "deepseek-reasoner"
STREAM = False
TEMPERATURE = 0.8
MAX_TOKENS = 10000

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL_NAME = "deepseek/deepseek-r1-0528:free"
RANKING_URL = None
RANKING_NAME = None
INCLUDE_REASONING = True



sources ="assets/"
# get the root path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = os.path.dirname(os.path.dirname(root_path))

# print(f"\n\n[ROOT_PATH]: {root_path} \n\n")
full_path = os.path.join(root_path, sources)
# print(f"\n\n[SOURCES]: {sources} \n\n")

VOWELS_DICT_PATH = full_path + "start_vowels.txt"
RHYME_DICT_PATH = full_path + "rhymes.txt"
TONE_DICT_PATH = full_path + "tone_dict.txt"
SPECIAL_TONE_DICT_PATH = full_path + "vocab_dupple_check.txt"
DICTIONARY_PATH = full_path + "words.txt"



CS_MASKED_WORDS = []
CS_IDX_MASKED_WORDS = set()
CS_TOKEN_MASKED_WORDS = "MASKED_WORD"

