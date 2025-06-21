import os 
import sys
import unicodedata

from typing import Optional, List, Dict, Union, Any
from ..configs import (
    MaskErrorTokenizationConfig,
    CountSyllablePoemsConfig,
)
from .poetic_rule import PoeticRules
from .count_syllables import CountSyllablePoems

class MaskErrorTokenization:
    def __init__(
            self,
            met_config: MaskErrorTokenizationConfig):
        super(MaskErrorTokenization, self).__init__()

        self.poetic_config = met_config.poetic_config
        self.count_syllable_config = met_config.count_syllable_config
        self.token_masked_words = self.count_syllable_config.token_masked_words
    

    def _run_poetic_rule(
            self, 
            poem_input: str,
            luc_bat: bool,
    ):
        """
            This is a function to check poetic rule if having any wrong or don't follow the rule,
            it will be marked as error before masking the token 

            Args:
                poem_input: stanza to check poetic rule
                luc_bat: whether or not the poem input is LỤC BÁT type poem or not
            
            Returns:


        """
        tags = "68" if luc_bat else "78"

        check_poetic_rule = PoeticRules(
            vowels_dict_path = self.poetic_config.vowels_dict_path, 
            rhyme_dict_path=self.poetic_config.rhyme_dict_path, 
            tone_dict_path=self.poetic_config.tone_dict_path, 
            dictionary_path=self.poetic_config.dictionary_path, 
            special_tone_dict_path=self.poetic_config.special_tone_dict_path
        )
        idx_masked_words, masked_words = check_poetic_rule.check_poem(
            poem=poem_input, 
            tag=tags
        )

        return idx_masked_words, masked_words

    def _run_count_syllables(
            self,
            poem_input: str,
            luc_bat: bool
    ):
        """
            Count syllables of a stanza at each line if not correct, it will be marked as error

            Args:
                stanza: stanza to check
                luc_bat: whether or not the stanza is LỤC BÁT type stanza or not

            Returns:

        """
        count_syllable_poems = CountSyllablePoems(
            config = CountSyllablePoemsConfig(
                    masked_words = self.count_syllable_config.masked_words,
                    idx_masked_words = self.count_syllable_config.idx_masked_words,
                    token_masked_words = self.count_syllable_config.token_masked_words
                )
        )
        idx_masked_words, masked_words = count_syllable_poems.count_syllables(
            stanza = poem_input,
            luc_bat = luc_bat
        )

        return idx_masked_words, masked_words

    def _check_luc_bat(
            self,
            poem_input: str
    ) -> bool:
        """
            Check if the stanza is LỤC BÁT type stanza or not

            Args:
                poem_input: poem to check

            Returns:
                luc_bat: whether or not the stanza is LỤC BÁT type stanza or not
        """
        #  Only check the first two line of the stanza
        luc_bat = False
        print(f"poem_input: {poem_input}")
        
        # sentences = poem_input.split("\n")[:2]
        # sentences_2 = poem_input.split("\n")[2:4]
        # print(f"sentences: {sentences}")

        # if len(sentences[0].strip().split(" ")) == 6 and len(sentences[1].strip().split(" ")) == 8:
        #     if len(sentences_2[0].strip().split(" ")) == 6 and len(sentences_2[1].strip().split(" ")) == 8:
        #         luc_bat = True
        lines = [line.strip() for line in poem_input.strip().split("\n") if line.strip()]
        print(f"2 first lines: {lines[:2]}")
        print(f"2 next lines: {lines[2:4]}")

        if len(lines) >= 4:
            if len(lines[0].split()) == 6 and len(lines[1].split()) == 8 \
            and len(lines[2].split()) == 6 and len(lines[3].split()) == 8:
                luc_bat = True

        return luc_bat
    
    def _run_masked_count_syllables(
              self,
              masked_poem_input: str,
              luc_bat: bool
    ) -> str:
        """
        A function mask (line_relatedSentence) token into the final masked poem

        Args:
            stanza: stanza to check
            luc_bat: whether or not the stanza is LỤC BÁT type stanza or not

        Returns:
            masked_poem(str): poem with error tokenization masked
        """ 
        first_sentence = True
        j = 1
        sentences = masked_poem_input.split("\n")
        for i, sentence in enumerate(sentences):
            if luc_bat:
                if first_sentence:
                    sentence = sentence + " " + f"(6_{j})"
                    first_sentence = False
                else:
                    sentence = sentence + " " + f"(8_{j})"
                    first_sentence = True
                    j += 1
            else:
                sentence = sentence + " " + f"(7_{i+1})"

            sentences[i] = sentence

        return "\n".join(sentences)

        

    def _run_masked_words(
            self,
            poem_input: str,
            idx_masked_words: List[int],
            masked_words: List[Dict[str, Any]],
            luc_bat: bool
    ):
        """ 
            A Function implement to mask error tokenization into the original stanza (poem input)

            Args:
                poem_input(str): poem input  to check
                idx_masked_words(Set(int)): index of masked words
                masked_words(List[Dict[str, Any]]): list of masked words

            Returns:
                masked_poem(str): poem with error tokenization masked
        """

        final_poem = ""
        
        sentences = poem_input.split("\n")
        for idx, masked_word in zip(idx_masked_words, masked_words):
            #  Split idx to get rows and cols (1_6) ==> rows = 1, cols = 6
            rows, cols = idx.split("_")[0], idx.split("_")[1]
            rows, cols = int(rows) - 1, int(cols) - 1

            if luc_bat:
                # Replace masked word phrase
                words = sentences[rows].split(" ")
                # Handle the wrong case if the stanza lack  or redundant word
                if masked_word["word"] == "missing":
                    # Replace missing word phrase
                    words.append(f"[{self.token_masked_words}]")

                elif masked_word["word"] == "reductant":
                    # Replace wrong word phrase
                    words[cols - 1:] = [f""]*2
                    words[cols] = f"[{self.token_masked_words}]"

                if rows % 2 == 0 and cols == 5:
                        words[cols - 1:] = [f"[{self.token_masked_words}]"]*2
                elif rows % 2 != 0 and cols == 5:
                        words[cols - 1:] = [f"[{self.token_masked_words}]"]*4
                else:
                    words[cols] = f"[{self.token_masked_words}]"

                # Join all words into the orignal sentence
                sentences[rows] = " ".join(words)
            
            else:
                # Replace masked word phrase
                words = sentences[rows].split(" ")
                # print(f"words: {words}")
                                # Handle the wrong case if the stanza lack  or redundant word
                if masked_word["word"] == "missing":
                    # print("missing")
                    # Replace missing word phrase
                    words.append(f"[{self.token_masked_words}]")
                elif masked_word["word"] == "reductant":
                    # Replace wrong word phrase
                    words[cols - 1:] = [f""]*2
                    words[cols] = f"[{self.token_masked_words}]"
                else:
                    words[cols] = f"[{self.token_masked_words}]"

                # Join all words into the orignal sentence
                sentences[rows] = " ".join(words)

        final_poem = "\n".join(sentences)
        return poem_input, final_poem

    def _check_error_vietnamese_words(
       self,
       poem_input: str
    ): 
        poem_input = unicodedata.normalize('NFC', poem_input)
        # Define valid Vietnamese letters and characters
        import re
        vietnamese_chars = (
            "aàáảãạăằắẳẵặâầấẩẫậ"
            "bcdđeèéẻẽẹêềếểễệ"
            "fgh"
            "iìíỉĩị"
            "jklmnoòóỏõọôồốổỗộơờớởỡợ"
            "pqrstuùúủũụưừứửữự"
            "vxyỳýỷỹỵ"
            "z"
            "AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ"
            "BCDĐEÈÉẺẼẸÊỀẾỂỄỆ"
            "FGH"
            "IÌÍỈĨỊ"
            "JKLMNOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ"
            "PQRSTUÙÚỦŨỤƯỪỨỬỮỰ"
            "VXYỲÝỶỸỴ"
            "Z"
        )

        # Also allow space, comma, period, colon, semicolon, dash, question/exclamation mark, quotes
        allowed_chars = set(vietnamese_chars + " ,.!?:;–\n\t\"'")


        # def mask_invalid_characters(text, allowed_chars, mask=self.token_masked_words):
        #     new_lines = []
        #     for line in text.strip().split("\n"):
        #         new_line = ""
        #         for ch in line:
        #             if ch not in allowed_chars:
        #                 new_line += "[{}]".format(mask)
        #             else:
        #                 new_line += ch
        #         new_lines.append(new_line)
        #     return "\n".join(new_lines)
                # === Function to mask entire words ===
        def mask_invalid_words(
                text: str, 
                allowed_chars: set, 
                mask: str = self.token_masked_words
        ) -> str:
            new_lines = []
            for line in text.strip().split("\n"):
                words = re.findall(r'\S+', line)  # split by spaces but preserve punctuation
                masked_line = []
                for word in words:
                    if all(char in allowed_chars for char in word):
                        masked_line.append(word)
                    else:
                        masked_line.append(f"[{mask}]")
                new_lines.append(' '.join(masked_line))
            return "\n".join(new_lines)

        # Apply masking
        masked_text = mask_invalid_words(poem_input, allowed_chars)
        def normalize_spaces(text: str) -> str:
            # Xử lý từng dòng riêng biệt, bỏ khoảng trắng đầu/cuối và chuẩn hóa khoảng trắng giữa từ
            lines = [re.sub(r"\s+", " ", line.strip()) for line in text.strip().split("\n")]
            return "\n".join(lines)

        # Apply normalization
        print(f"Normalizing spaces...")
        masked_text = normalize_spaces(masked_text)


        # Output
        return masked_text




    def mask_error_tokenization(
            self,
            poem_input: str
    ):
        """
            This is a main function to mask error tokenization

            Args:
                stanza: stanza to check
                luc_bat: whether or not the stanza is LỤC BÁT type stanza or not

            Returns:
                masked_poem: poem with error tokenization masked
        """
        # Check Vietnamese words
        print(f"poem input before check: {poem_input}")
        poem_input = self._check_error_vietnamese_words(poem_input = poem_input)
        print(f"poem input after check: {poem_input}")
        # check luc bat
        luc_bat = self._check_luc_bat(poem_input = poem_input)
        print(f"LUC BÁT TYPE: {luc_bat}")

        # count syllables
        cs_idx_masked_words, cs_masked_words = self._run_count_syllables(
            poem_input = poem_input,
            luc_bat = luc_bat
        )

        # check poetic rule
        pr_idx_masked_words, pr_masked_words = self._run_poetic_rule(
            poem_input = poem_input,
            luc_bat = luc_bat
        )

        # combine all errors of count syllables and poetic rule problems
        combined_idx_masked_words = set()
        combined_idx_masked_words.update(cs_idx_masked_words)
        combined_idx_masked_words.update(pr_idx_masked_words)
        combined_masked_words = pr_masked_words + cs_masked_words

        print(f" cs_idx_masked_words: {cs_idx_masked_words} \n cs_masked_words: {cs_masked_words} \n pr_idx_masked_words: {pr_idx_masked_words} \n pr_masked_words: {pr_masked_words} \n")
        print(f" combined_idx_masked_words: {combined_idx_masked_words} \n combined_masked_words: {combined_masked_words} \n")
        # print(sorted(list(combined_idx_masked_words)))

        # Sort combined_idx_masked_words
        combined_idx_masked_words_sorted = sorted(
            combined_idx_masked_words,
            key=lambda x: tuple(map(int, x.split('_')))
        )

        # Sort combined_masked_words by line and position
        combined_masked_words_sorted = sorted(
            combined_masked_words,
            key=lambda x: (x['line'], x['position'])
        )
        print(f"combined_idx_masked_words_sorted: {combined_idx_masked_words_sorted} \n combined_masked_words_sorted: {combined_masked_words_sorted} \n")

        poem_input, masked_poem = self._run_masked_words(
            poem_input = poem_input,
            idx_masked_words = combined_idx_masked_words_sorted,
            masked_words = combined_masked_words_sorted,
            luc_bat = luc_bat
        )

        return poem_input, luc_bat,  self._run_masked_count_syllables(
            masked_poem_input = masked_poem,
            luc_bat = luc_bat
        )


