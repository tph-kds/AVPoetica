import os 
import sys

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
        sentences = poem_input.split("\n")[:2]
        print(f"sentences: {sentences}")

        if len(sentences[0].strip().split(" ")) == 6 and len(sentences[1].strip().split(" ")) == 8:
            luc_bat = True

        return luc_bat

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

        print(f"cs_idx_masked_words: {cs_idx_masked_words} \n cs_masked_words: {cs_masked_words} \n pr_idx_masked_words: {pr_idx_masked_words} \n pr_masked_words: {pr_masked_words} \n")



