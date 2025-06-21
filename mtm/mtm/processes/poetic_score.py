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


from ..configs import PoeticRulesMetricsConfig

def load_data(filename: str):

    with open(filename, 'r', encoding='utf-8') as file:
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
  def __init__(
      self,
      metrics_config: PoeticRulesMetricsConfig
    ):
    """
      Constructor for RhymesTonesMetrics class

      Params:
        vowels_dict_path: path to vowels dictionary
        rhyme_dict_path: path to rhyme dictionary
        tone_dict_path: path to tone dictionary
        dictionary_path: path to dictionary
        special_tone_dict_path: path to special tone dictionary

    """

    self.even_chars, self.list_start_vowels, self.tones = vowels(metrics_config.vowels_dict_path)
    self.rhymes_dict = rhyme(metrics_config.rhyme_dict_path)
    self.tone_dict = tone(metrics_config.tone_dict_path)
    self.dictionary_vi = dictionary(metrics_config.dictionary_path)
    self.special_tone_dict = special_tone(metrics_config.special_tone_dict_path)

  def is_stanza(self, sentences: str):
      """
        Check if input is a stanza or not

        param sentences: sentences to check

        return: is stanza or not
      """
      return len(sentences.split("\n\n")) == 1

  def split_special_char(self, word: str):
    """
        Split word by special char

        param word: word to split

        return: a complete word
        Ex: hương... -> hương
    """
    special_chars = re.split(r"[^\w\s]", word)
    return special_chars[0]


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



  def check_rhyme_pair(
      self,
      prev_sentence: str,
      cur_sentence: str,
      check_ryhme_label,
      tag: str,
      prev_end_words_rhyme="",
  ):
      """
          Check 2 words rhyme if the same

          param word1, word2: words to check

          return: is the same rhyme or not
        """
      rhyme_errors = 0
      length_errors = 0

      prev_length = len(prev_sentence.split(" "))
      cur_length = len(cur_sentence.split(" "))

      tag_end_word = 0 # index of ending word to check ryhme

      if tag == "68":
        tag_end_word = 5

        if prev_length != 6:
            prev_sentence = "(L)" + prev_sentence
            length_errors = length_errors + 1

        if cur_length != 8:
            cur_sentence = "(L)" + cur_sentence
            length_errors = length_errors + 1

      elif tag == "78":
        tag_end_word = 6

        if prev_length != 7:
            prev_sentence = "(L)" + prev_sentence
            length_errors = length_errors + 1

        if cur_length != 7:
            cur_sentence = "(L)" + cur_sentence
            length_errors = length_errors + 1

      prev_words = prev_sentence.split(" ")
      cur_words = cur_sentence.split(" ")

      prev_words_in_sentences = self.split_special_char(prev_words[tag_end_word])
      cur_words_in_sentences = self.split_special_char(cur_words[tag_end_word])
      prev_end_words_rhyme = self.split_special_char(prev_end_words_rhyme)

      if prev_end_words_rhyme == "":
          try:
              if not self.compare(prev_words_in_sentences, cur_words_in_sentences):

                  cur_words[tag_end_word] = cur_words[tag_end_word] + "(E_V)"
                  check_ryhme_label = "(E_V)"
                  rhyme_errors = rhyme_errors + 1
              else:
                  check_ryhme_label = "(R)"

          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

      if prev_end_words_rhyme != "":
          try:
            if not self.compare(prev_words_in_sentences, prev_end_words_rhyme):

                prev_words[tag_end_word] = prev_words[tag_end_word] + "(E_V)"
                check_ryhme_label = "(E_V)"
                rhyme_errors = rhyme_errors + 1
            else:
                check_ryhme_label = "(R)"

          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

          try:
            if not self.compare(prev_end_words_rhyme, cur_words_in_sentences):

                cur_words[tag_end_word] = cur_words[tag_end_word] + "(E_V)"
                check_ryhme_label = "(E_V)"
                rhyme_errors = rhyme_errors + 1
            else:
                check_ryhme_label = "(R)"


          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

      prev_sentence = " ".join(prev_words)
      cur_sentence = " ".join(cur_words)


      return prev_sentence, cur_sentence, cur_words[-1], rhyme_errors, length_errors, check_ryhme_label

  def check_ryhme_stanze_type_78(
      self,
      sentences: str,
      first_words: str,
      prev_end_words_rhyme: str,
      total_rhyme_errors: int,
      total_length_errors: int,
      check_ryhme_label,
      check_ryhme_labels,
      tag: str
  ):
      """
        Check rhyme by stanza with THAT NGON BAT CU type

        Params:
          sentence: List of sentences in stanza
          first_words: List of first words in sentences
          prev_end_words_rhyme: ending word of previous sentence
          total_rhyme_errors: total rhyme errors
          total_length_errors: total length errors
          check_ryhme_label: check rhyme label
          check_ryhme_labels: list of check rhyme labels
          tag: tag Input - type of poem

        Returns:
          res: stanza after check filter and error highlighted
          total_rhyme_errors: total rhyme errors
          total_length_errors: total length errors
          check_ryhme_labels: list of check rhyme labels
      """

      ryhme_sentence_lines = [0]
      out_ryhme_sentence_lines = []

      for i in range(int(len(sentences)/2)):
        ryhme_sentence_lines = ryhme_sentence_lines + [int(2*i+1)]
        out_ryhme_sentence_lines = out_ryhme_sentence_lines + [int(2*i)]
      out_ryhme_sentence_lines = out_ryhme_sentence_lines[1:]

      # print(out_ryhme_sentence_lines, ryhme_sentence_lines)


      if len(first_words) == 7:
          prev_end_words_rhyme = self.split_word(first_words[6])

      for i in range(0, len(ryhme_sentence_lines) - 1):
          idx = ryhme_sentence_lines[i]
          idx_next = ryhme_sentence_lines[i+1]

          sentences[idx], sentences[idx_next], prev_end_words_rhyme, rhyme_errors, length_errors, check_ryhme_label =\
              self.check_rhyme_pair(sentences[idx], sentences[idx_next], check_ryhme_label, tag, prev_end_words_rhyme)

          total_rhyme_errors = total_rhyme_errors + rhyme_errors
          total_length_errors = total_length_errors + length_errors

          check_ryhme_labels[idx_next] = check_ryhme_label

      return "\n".join(sentences), total_rhyme_errors, total_length_errors, check_ryhme_labels

  def check_rhyme_stanza_type_68(
      self,
      sentences: str,
      first_words: str,
      prev_end_words_rhyme: str,
      total_rhyme_errors: int,
      total_length_errors: int,
      check_ryhme_label,
      check_ryhme_labels,
      start_index: int,
      tag: str
  ):
      """
        Check rhyme by stanza with LUC BAT type

        Params:
          sentence: List of sentences in stanza
          first_words: List of first words in sentences
          prev_end_words_rhyme: ending word of previous sentence
          total_rhyme_errors: total rhyme errors
          total_length_errors: total length errors
          check_ryhme_label: check rhyme label
          check_ryhme_labels: list of check rhyme labels
          start_index: start index of sentences
          tag: tag Input - type of poem

        Returns:
          res: stanza after check filter and error highlighted
          total_rhyme_errors: total rhyme errors
          total_length_errors: total length errors
          check_ryhme_labels: list of check rhyme labels

      """

      if len(first_words) == 8:
          prev_end_words_rhyme = self.split_word(first_words[7])
          start_index = 1

      for i in range(start_index, len(sentences), 2):
          if i+1 == len(sentences):
              sentences.append("Missing ending sentence")
          sentences[i], sentences[i+1], prev_end_words_rhyme, rhyme_errors, length_errors, check_ryhme_label =\
              self.check_rhyme_pair(sentences[i], sentences[i + 1], check_ryhme_label, tag, prev_end_words_rhyme)
          total_rhyme_errors = total_rhyme_errors + rhyme_errors
          total_length_errors = total_length_errors + length_errors

          check_ryhme_labels[i+1] = check_ryhme_label

      return "\n".join(sentences), total_rhyme_errors, total_length_errors, check_ryhme_labels

  def check_rhyme_stanza(
      self,
      stanza: str,
      tag: str
  ):
      """
          Check rhyme by stanza

          Params:
            stanza: input stanza to check
            tag: tag Input - type of poem

          Returns:
            res: stanza after check filter and error highlighted
            total_rhyme_errors: total rhyme errors
            total_length_errors: total length errors

        """
      sentences = stanza.split("\n")
      first_words = sentences[0].split(" ")
      start_index = 0
      prev_end_words_rhyme = ""
      total_rhyme_errors = 0
      total_length_errors = 0
      check_ryhme_labels = [""]*len(sentences)
      # Init original value
      check_ryhme_labels[0] = "(R)"
      check_ryhme_label = ""

      if tag == "78":

        res, total_rhyme_errors, total_length_errors, check_ryhme_labels = self.check_ryhme_stanze_type_78(
            sentences,
            first_words,
            prev_end_words_rhyme,
            total_rhyme_errors,
            total_length_errors,
            check_ryhme_label,
            check_ryhme_labels,
            tag
        )
      elif tag == "68":
        res, total_rhyme_errors, total_length_errors, check_ryhme_labels = self.check_rhyme_stanza_type_68(
            sentences,
            first_words,
            prev_end_words_rhyme,
            total_rhyme_errors,
            total_length_errors,
            check_ryhme_label,
            check_ryhme_labels,
            start_index,
            tag
        )
      else:
        pass


      return res, total_rhyme_errors, total_length_errors, check_ryhme_labels


  def get_tone(self, word: str):
      """
            Check word is even tone or not

            param word: word to check tone

            return: even or uneven
          """
          # i, e, ê, o, ô, ơ, a,  ă, â, u, ư, y
      first_char = self.split_word(word)
      suffix_char = first_char
      len_char = len(first_char)
      first_char = first_char[0]
      flag = 0
      if first_char in self.special_tone_dict:
        # hòa, nước => ước
        if first_char in self.even_chars:
          flag += 0
        elif first_char in self.special_tone_dict and first_char not in self.even_chars:
          flag += 1
        ### Check the second
        for l in range(1, len_char):
          second_char = suffix_char[l]
          if second_char in self.even_chars:
            flag += 0
          elif second_char in self.special_tone_dict and second_char not in self.even_chars:
            flag += 1
        flag = flag / len_char
        if flag > 0: # if have existed a char with uneven ==> uneven
          return 'uneven'
        else:
          return 'even'

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

  def check_tone_sentence(
      self,
      sentence: str,
      row_sentence: int,
      first_tone_default: list,
      tag: str
  ):
      """
          Check sentence is on the right form of even or uneven rule

          param sentence: sentence to check tone

          return: sentences after added notation to highlight error
                  total_wrong_tone: total wrong tone in sentence
        """
      words = sentence.split(" ")
      length = len(words)
      cur_tone_dict = None
      sentence_correct = words

      ## Check the format Tone of each sentence
      if tag == "78":
        ## 78
        if length != 7:
            return "(L)"+sentence, 0, " ".join(sentence_correct)

        if row_sentence in first_tone_default[0]:
          cur_tone_dict = self.tone_dict[length]
        elif row_sentence in first_tone_default[1]:
          number_tone = int((str(length) + "1"))
          cur_tone_dict = self.tone_dict[number_tone]

      elif tag == "68":
        ## 68
        if length != 6 and length != 8:
            return "(L)"+sentence, 0, " ".join(sentence_correct)
        cur_tone_dict = self.tone_dict[length]
      total_wrong_tone = 0
      for i in cur_tone_dict:
          if self.get_tone(words[i]) != cur_tone_dict[i]:
              total_wrong_tone = total_wrong_tone + 1
              words[i] = words[i] + "(E_T)"
          else:
            if self.get_tone(words[i]) == 'uneven':
              sentence_correct[i] = sentence_correct[i] + "(T)"
            elif self.get_tone(words[i]) == 'even':
              sentence_correct[i] = sentence_correct[i] + "(B)"

      return " ".join(words), total_wrong_tone, " ".join(sentence_correct)


  def check_tone_stanza(
      self,
      stanza: str,
      tag: str
  ):
      """
          Check stanza is on the right form of even or uneven rule

          Params:
            sentence: stanza to check tone
            tag: tag Input - type of poem

          Returns:
            stanza after added notation to highlight error
            total_wrong_tone: total wrong tone in sentence
        """
      sentences = stanza.split("\n")
      sentences_correct = []
      total_wrong = 0
      ### the first Define for the tone of the first sentence is _ T _ B _ T _ _
      first_tone_default = [[0, 3, 4, 7], [1, 2, 5, 6]] ## ==> 7 ffile, 71 file
      first_sentence_words_1 = sentences[0].split(" ")[1]
      # Check even , uneven for a sentence
      if self.get_tone(first_sentence_words_1) == 'uneven':
        first_tone_default_sentence = first_tone_default
      elif self.get_tone(first_sentence_words_1) == 'even':
        first_tone_default_sentence = [first_tone_default[1], first_tone_default[0]]

      for i in range(len(sentences)):
          current_wrong = 0

          sentences[i], current_wrong, sentence_correct = self.check_tone_sentence(sentences[i], i, first_tone_default_sentence, tag)
          total_wrong = total_wrong + current_wrong
          sentences_correct.append(sentence_correct)
      return "\n".join(sentences), total_wrong, "\n".join(sentences_correct)


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


  def check_rule(
      self,
      stanza: str,
      tag: str
  ):
      """
        A function to check both rhyme and tone rule

        Params:
            sentence: stanza to check
            tag: tag Input - type of poem

        Returns:
            stanza processed
      """
      if not self.is_stanza(stanza):
          print(stanza + ": is not a stanza")
          return
      stanza = self.preprocess_stanza(stanza)
      stanza, total_rhyme_errors, total_length_errors, check_ryhme_labels = self.check_rhyme_stanza(stanza, tag) # Create and record error unstructured sentences
      stanza, total_wrong_tone, sentences_correct_format = self.check_tone_stanza(stanza, tag)

      each_sentence = sentences_correct_format.split("\n")
      mixed_format = [""]*len(each_sentence)
      for i in range(len(each_sentence)):
          mixed_format[i] = each_sentence[i] + check_ryhme_labels[i]

      mixed_format = "\n".join(mixed_format)
      return stanza, total_length_errors, total_rhyme_errors, total_wrong_tone, mixed_format

  def check_spelling_vietnamese(
      self,
      stanza: str,
      total_spelling_errors: int,
      sentences_correct_format: str,
      recommend_correct_format: dict
  ):
      """

         A function to check Spelling Rule VietNamese Language

         Params:
            sentence: stanza to check
            total_spelling_errors: total spelling errors


         Returns:
            stanza processed
            total_spelling_errors: total spelling errors
            sentences_correct_format: sentences after added notation to highlight error
      """

      sentences = stanza.split("\n")
      for sentence in sentences:
          words = sentence.split(" ")
          words_out = []
          for word in words:
            first_char = word[0].lower()
            vietnamese_chars = self.dictionary_vi[first_char]
            if self.split_special_char(word.lower()) in vietnamese_chars:
              continue
            else:
              total_spelling_errors = total_spelling_errors + 1
              word = word + "(E_S)"
              recommend_correct_format[word] = vietnamese_chars
            words_out.append(word)
          sentences_correct_format.append(" ".join(words_out))
      # print(sentences_correct_format)
      return total_spelling_errors, "\n".join(sentences_correct_format), recommend_correct_format


  def calculate_score_by_error(self,
      stanza_length: int,
      tag: str,
      total_length_errors: int,
      total_rhyme_errors: int,
      total_wrong_tone: int,
      total_spelling_errors: int,
      total_length_words_of_stanza,
  ):
      """
        A function to calculate score for the Stanza by length, rhyme and tone errors
            Currently doesnt punish the length error

        Params:
              sentence: stanza_length,
                        total_length_errors,
                        total_rhyme_errors,
                        total_wrong_tone
              tag: tag Input - type of poem

        Returns:

          Score: score calculated by formula that rhyme accounts for 70% score rate and 30% left for tone
      """
      num_first_sentence = ceil(stanza_length/2)
      num_second_sentence = floor(stanza_length/2)
      total_length_rhyme_errors = 0.00001
      total_length_tone_errors = 0.00001

      if tag == "68": # Thơ Luc Bat
          total_length_rhyme_errors = (num_first_sentence + 2*num_second_sentence-1)
          total_length_tone_errors = (3*num_first_sentence+4*num_second_sentence)
      elif tag =="78": # Thơ That Ngon Bat Cu
          total_length_rhyme_errors = (num_first_sentence + num_second_sentence-3)
          total_length_tone_errors = (3*num_first_sentence+3*num_second_sentence)
      elif tag == "00":
          # total_length_words_of_stanza = stanza_length
          return 100 - 100 * (total_spelling_errors/ total_length_words_of_stanza)
      else:
        pass

      rhyme_minus_points = 70*total_rhyme_errors/total_length_rhyme_errors
      tone_minus_points = 30*total_wrong_tone/total_length_tone_errors

      return 100 - rhyme_minus_points - tone_minus_points


  def calculate_stanza_score(self,
                             stanza: str,
                             tag: str):
      """
        A function to calculate score for the Stanza

        param sentence: stanza

        return: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
          and 30% left for tone
      """

      stanza = self.preprocess_stanza(stanza)
      length = len(stanza.split("\n"))
      total_length_errors = 0
      total_rhyme_errors = 0
      total_wrong_tone = 0
      total_spelling_errors = 0

      word_by_stanza = [ x.split(" ") for x in stanza.split("\n")]
      # Concatenate into a single list
      flat_list = [item for item in chain.from_iterable(word_by_stanza) if item]
      total_length_words_of_stanza = len(flat_list)
      sentences_correct_format = []
      recommend_correct_format = {}
      try:
        if tag != "00":
          stanza, total_length_errors, total_rhyme_errors, total_wrong_tone, sentences_correct_format = self.check_rule(stanza, tag)
        elif tag == "00":
          total_spelling_errors, sentences_correct_format, recommend_correct_format = self.check_spelling_vietnamese(stanza, total_spelling_errors, sentences_correct_format, recommend_correct_format)

        score = self.calculate_score_by_error(length, tag, total_length_errors, total_rhyme_errors, total_wrong_tone, total_spelling_errors, total_length_words_of_stanza)


      except Exception as e:
          print(e)
          score = 0
          sentences_correct_format = ""
      return score, sentences_correct_format, recommend_correct_format


  def calculate_score(self,
                      poem: str,
                      tag: str):
      """
        A function to calculate score for a poem that may have some stanzas

        Params:
          sentence: poem Input
          tags: tags Input - type of poem

        Returns:
          score_accuracy_poemn: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
        and 30% left for tone

      """
      sum_ = 0
      count = 0
      sentences_correct_format = ""
      recommend_correct_format = {}
      for i in poem.split("\n\n"):
          count += 1
          score, sentences_correct_format, recommend_correct_format = self.calculate_stanza_score(i, tag)
        #   print(sentences_correct_format)
        #   print(recommend_correct_format)
          sum_ = sum_ + score
      return sum_/count




