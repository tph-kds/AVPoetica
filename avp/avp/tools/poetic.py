# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" The 'poetic' tool for several agents to affect session states."""

import os 
from typing import Dict, List, Any 
from google.adk.tools import ToolContext
from ..configs import (
    PoeticScoreToolInput,
    PoeticScoreToolOutput
)
import requests

import re
import ast
import json
from math import ceil, floor
from collections import defaultdict
from itertools import chain


try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

sources ="avp/avp/tools/assets/"

def load_data(filename: str):

    with open(filename, 'r') as file:
        text = file.read()

    content = ast.literal_eval(text)
    return content
def vowels(vowels_path: str):
    even_chars = []
    list_start_vowels = []
    tones = {}
    thanhtrac = []
    thanhbang = []
    start_vowels = load_data(vowels_path)


    huyen = start_vowels['huyen']
    sac = start_vowels['sac']
    nang = start_vowels['nang']
    hoi = start_vowels['hoi']
    nga = start_vowels['nga']
    khong_dau = start_vowels['khong_dau']

    thanhbang.extend(huyen)
    thanhbang.extend(khong_dau)
    thanhtrac.extend(sac)
    thanhtrac.extend(nang)
    thanhtrac.extend(hoi)
    thanhtrac.extend(nga)
    tones["thanhtrac"] = thanhtrac
    tones["thanhbang"] = thanhbang

    list_start_vowels.extend(huyen)
    list_start_vowels.extend(sac)
    list_start_vowels.extend(nang)
    list_start_vowels.extend(hoi)
    list_start_vowels.extend(nga)
    list_start_vowels.extend(khong_dau)

    even_chars.extend(huyen)
    even_chars.extend(khong_dau)
    return even_chars, list_start_vowels, tones

def rhyme(rhyme_path: str):
    # rhyme_path = sources + "rhymes.txt"
    rhymes_dict = load_data(rhyme_path)
    return rhymes_dict

def tone(tone_path: str):
    # tone_path = sources + "tone_dict.txt"
    tone_dict = load_data(tone_path)
    return tone_dict

def special_tone(special_tone_path: str):
    # tone_path = sources + "vocab_dupple_check.txt"
    special_tone_dict = load_data(special_tone_path)
    return special_tone_dict

def dictionary(dictionary_path: str):
    # dictionary_path = sources + "words.txt"
    word_dict = defaultdict(set)

    with open(dictionary_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = json.loads(line.strip())
            text = entry["text"].lower()

            first_char = text[0].lower()
            word_dict[first_char].add(text)

    result_dict = dict(word_dict)
    return result_dict


class RhymesTonesMetrics:
  def __init__(self, vowels_dict_path, rhyme_dict_path, tone_dict_path):
    self.even_chars, self.list_start_vowels = vowels(vowels_dict_path)
    self.rhymes_dict = rhyme(rhyme_dict_path)
    self.tone_dict = tone(tone_dict_path)

  def is_stanza(self, sentences: str):
      """
        Check if input is a stanza or not

        param sentences: sentences to check

        return: is stanza or not
      """
      return len(sentences.split("\n\n")) == 1


  def split_word(self, word):
      """
          Split word by 2 part, starting and ending

          param word: word to split

          return: ending part of word
          Ex: mùa -> ùa
      """
      word_length = len(word)
      start_index = 0
      prev = ''
      for i in range(word_length):
          if prev == 'g' and word[i] == 'i':
              continue
          if prev == 'q' and word[i] == 'u':
              continue
          if word[i] in self.list_start_vowels:
              start_index = i
              break
          prev = word[i]
      return word[start_index:]


  def compare(self, word1: str, word2: str):
      """
        Check 2 words rhyme if the same

        param word1, word2: words to check

        return: is the same rhyme or not
      """
      rhyme1 = self.split_word(word1)
      rhyme2 = self.split_word(word2)

      if rhyme2 in self.rhymes_dict[rhyme1]:
          return True
      return False


  def check_rhyme_pair(self, prev_sentence: str, cur_sentence: str, prev_eight_words_rhyme=""):
      """
          Check 2 words rhyme if the same

          param word1, word2: words to check

          return: is the same rhyme or not
        """
      rhyme_errors = 0
      length_errors = 0

      prev_length = len(prev_sentence.split(" "))
      cur_length = len(cur_sentence.split(" "))

      if prev_length != 6:
          prev_sentence = "(L)" + prev_sentence
          length_errors = length_errors + 1
          print(1)

      if cur_length != 8:
          cur_sentence = "(L)" + cur_sentence
          length_errors = length_errors + 1

      prev_words = prev_sentence.split(" ")
      cur_words = cur_sentence.split(" ")

      if prev_eight_words_rhyme == "":
          try:
              if not self.compare(prev_words[5], cur_words[5]):
                  cur_words[5] = cur_words[5] + "(V)"
                  rhyme_errors = rhyme_errors + 1
          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass
      if prev_eight_words_rhyme != "":
          try:
              if not self.compare(prev_words[5], prev_eight_words_rhyme):
                  prev_words[5] = prev_words[5] + "(V)"
                  rhyme_errors = rhyme_errors + 1
          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass
          try:
              if not self.compare(prev_eight_words_rhyme, cur_words[5]):
                  cur_words[5] = cur_words[5] + "(V)"
                  rhyme_errors = rhyme_errors + 1
          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass
      prev_sentence = " ".join(prev_words)
      cur_sentence = " ".join(cur_words)

      return prev_sentence, cur_sentence, cur_words[-1], rhyme_errors, length_errors


  def check_rhyme_stanza(self, stanza: str):
      """
          Check rhyme by stanza

          param stanza: input stanza to check

          return: res: stanza after check filter and error highlighted
                  total_rhyme_errors: total rhyme errors
                  total_length_errors: total length errors
        """
      sentences = stanza.split("\n")
      first_words = sentences[0].split(" ")
      start_index = 0
      prev_eight_words_rhyme = ""
      total_rhyme_errors = 0
      total_length_errors = 0

      if len(first_words) == 8:
          prev_eight_words_rhyme = self.split_word(first_words[7])
          start_index = 1

      for i in range(start_index, len(sentences), 2):
          if i+1 == len(sentences):
              sentences.append("Missing ending sentence")
          sentences[i], sentences[i+1], prev_eight_words_rhyme, rhyme_errors, length_errors =\
              self.check_rhyme_pair(sentences[i], sentences[i + 1], prev_eight_words_rhyme)
          total_rhyme_errors = total_rhyme_errors + rhyme_errors
          total_length_errors = total_length_errors + length_errors
      res = "\n".join(sentences)
      return res, total_rhyme_errors, total_length_errors


  def get_tone(self, word: str):
      """
            Check word is even tone or not

            param word: word to check tone

            return: even or uneven
          """
      first_char = self.split_word(word)
      first_char = first_char[0]
      for i in self.even_chars:
          if first_char == i:
              return 'even'
      try:
          second_char = first_char[1]
          for i in self.even_chars:
              if second_char == i:
                  return 'even'
      except:
          pass
      return 'uneven'


  def check_tone_sentence(self, sentence: str):
      """
          Check sentence is on the right form of even or uneven rule

          param sentence: sentence to check tone

          return: sentences after added notation to highlight error
                  total_wrong_tone: total wrong tone in sentence
        """
      words = sentence.split(" ")
      length = len(words)
      if length != 6 and length != 8:
          return "(L)"+sentence, 0
      cur_tone_dict = self.tone_dict[length]
      total_wrong_tone = 0
      for i in cur_tone_dict:
          if self.get_tone(words[i]) != cur_tone_dict[i]:
              total_wrong_tone = total_wrong_tone + 1
              words[i] = words[i] + "(T)"
      return " ".join(words), total_wrong_tone


  def check_tone_stanza(self, stanza: str):
      """
          Check stanza is on the right form of even or uneven rule

          param sentence: stanza to check tone

          return: stanza after added notation to highlight error
                  total_wrong_tone: total wrong tone in sentence
        """
      sentences = stanza.split("\n")
      total_wrong = 0
      for i in range(len(sentences)):
          current_wrong = 0
          sentences[i], current_wrong = self.check_tone_sentence(sentences[i])
          total_wrong = total_wrong + current_wrong
      return "\n".join(sentences), total_wrong


  def preprocess_stanza(self, stanza: str):
      """
        A function to process Stanza to remove all unnecessary blank

        param sentence: stanza to process

        return: stanza processed
      """
      sentences = stanza.split("\n")
      sentences_out = []
      for sentence in sentences:
          words = sentence.split(" ")
          words_out = []
          for word in words:
              if word:
                  words_out.append(word)
          sentences_out.append(" ".join(words_out))
      return "\n".join(sentences_out)


  def check_rule(self, stanza: str):
      """
        A function to check both rhyme and tone rule

        param sentence: stanza to check

        return: stanza processed
      """
      if not self.is_stanza(stanza):
          print(stanza + ": is not a stanza")
          return
      stanza = self.preprocess_stanza(stanza)
      stanza, total_rhyme_errors, total_length_errors = self.check_rhyme_stanza(stanza) # Create and record error unstructured sentences
      stanza, total_wrong_tone = self.check_tone_stanza(stanza)
      return stanza, total_length_errors, total_rhyme_errors, total_wrong_tone


  def calculate_score_by_error(self, stanza_length: int, total_length_errors=0, total_rhyme_errors=0, total_wrong_tone=0):
      """
        A function to calculate score for the Stanza by length, rhyme and tone errors
            Currently doesnt punish the length error

        param sentence: stanza_length,
                        total_length_errors,
                        total_rhyme_errors,
                        total_wrong_tone

        return: score calculated by formula that rhyme accounts for 70% score rate and 30% left for tone
      """

      num_six = ceil(stanza_length/2)
      num_eight = floor(stanza_length/2)

      rhyme_minus_points = 70*total_rhyme_errors/(num_six + 2*num_eight-1)
      tone_minus_points = 30*total_wrong_tone/(3*num_six+4*num_eight)

      return 100 - rhyme_minus_points - tone_minus_points


  def calculate_stanza_score(self, stanza: str):
      """
        A function to calculate score for the Stanza

        param sentence: stanza

        return: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
          and 30% left for tone
      """

      stanza = self.preprocess_stanza(stanza)
      length = len(stanza.split("\n"))

      try:
          stanza, total_length_errors, total_rhyme_errors, total_wrong_tone = self.check_rule(stanza)

          score = self.calculate_score_by_error(length, total_length_errors, total_rhyme_errors, total_wrong_tone)
      except Exception as e:
          print(e)
          score = 0
      return score


  def calculate_score(self, poem: str):
      """
        A function to calculate score for a poem that may have some stanzas

        param sentence: poem

        return: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
        and 30% left for tone
      """
      sum_ = 0
      count = 0
      for i in poem.split("\n\n"):
          count += 1
          sum_ = sum_ + self.calculate_stanza_score(i)
      return sum_/count


def _score(
        poem: str,
        luc_bat: bool = False,
        sources: str = "./avp/tools/assets/"
):
    """
    A function to calculate score for a poem that may have some stanzas

    param sentence: poem

    return: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
    and 30% left for tone
    """
    vowels_path = sources + "start_vowels.txt"
    rhyme_path = sources + "rhymes.txt"
    tone_path = sources + "tone_dict.txt"
    special_tone_path = sources + "vocab_dupple_check.txt"
    dictionary_path = sources + "words.txt"

    # even_chars, list_start_vowels, tones = vowels(vowels_path)
    # rhymes_dict = rhyme(rhyme_path)
    # tone_dict = tone(tone_path)
    # special_tone_dict = special_tone(special_tone_path)
    # dictionary_vi = dictionary(dictionary_path)

    metrics = RhymesTonesMetrics(vowels_path, rhyme_path, tone_path, dictionary_path, special_tone_path)
    tags = "68" if luc_bat else "78"
    score = metrics.calculate_score(luc_bat, tag=tags)
    return score if score > 0.0 else 0.0



def poetic_score(configs: PoeticScoreToolInput) -> PoeticScoreToolOutput:
    """The 'poetic' tool for several agents to affect session states."""

    response_status = "failed"
    response_score = 0.0
    target_score = 0.95

    tool_context = ToolContext.from_state(configs.key)
    poem_input = tool_context.poem_input
    is_luc_bat = True if tool_context.poetic_form.lower() ==  "luc bat" or tool_context.poetic_form.lower() == "lục bát" else False
    score = _score(
        poem=poem_input,
        luc_bat=is_luc_bat
    )
    if score is not None:
        tool_context.state["score_checker_output"]["score"] = score

    if tool_context.state["score_checker_output"]["score"] is not None:
        response_status = "pending"
        response_score = tool_context.state["score_checker_output"]["score"]
        if response_score > target_score:
            response_status = "completed"
            tool_context.actions.escalate = True
        else:
            response_status = "pending"
            tool_context.actions.escalate = False

    return PoeticScoreToolOutput(
        status=response_status,
        state=tool_context.state,
        poetic_score=response_score,
    )



#   [
    # "Cởi trần gian, cởi hết ra \nHờn ai phai nhạt, xót xa nghẹn ngào. \nSương pha mái bạc, áo bào, \nThế gian bể khổ, lệ trào xót thương. \nNhớ chăng quê cũ dặm trường, \nTóc thề vương vấn, má hường phôi pha. \nTrăng tàn canh vắng, lệ sa, \nÂm thầm ôm bóng, xót xa cõi lòng."
#   ]