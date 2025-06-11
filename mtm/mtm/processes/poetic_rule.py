import re
import ast
import json
from math import ceil, floor
from collections import defaultdict
from itertools import chain
from typing import Optional


try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

sources ="assets/"

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


class PoeticRules:
  def __init__(
      self,
      vowels_dict_path,
      rhyme_dict_path,
      tone_dict_path,
      dictionary_path,
      special_tone_dict_path
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

    self.even_chars, self.list_start_vowels, self.tones = vowels(vowels_dict_path)
    self.rhymes_dict = rhyme(rhyme_dict_path)
    self.tone_dict = tone(tone_dict_path)
    self.dictionary_vi = dictionary(dictionary_path)
    self.special_tone_dict = special_tone(special_tone_dict_path)


    self.masked_words = [
        #  {
        #     "line": 1,
        #     "position": 8,
        #     "word": "mùa"
        #  },
      ]
    self.idx_masked_words = set()
    self.token_masked_words = "MASKED_WORD"

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


  def add_masked_word(
        self, 
        word: str,
        line: int,
        position: int
  ):
      self.masked_words.append({
          "line": line,
          "position": position,
          "word": word
      })

      self.idx_masked_words.add(f"{line}_{position}") # ex: 1_8 for line 1, position 8
      

      print(f"Masked word: {word} at line {line}, position {position}")



  def check_rhyme_pair(
      self,
      prev_sentence: str,
      cur_sentence: str,
      idx: int,
      idx_next: int,
      tag: str,
      prev_end_words_rhyme="",
  ):
      """
          Check 2 words rhyme if the same

          param word1, word2: words to check

          return: is the same rhyme or not
        """
      error_word = ""

      tag_end_word = 0 # index of ending word to check ryhme

      if tag == "68":
        tag_end_word = 5

      elif tag == "78":
        tag_end_word = 6

      prev_words = prev_sentence.split(" ")
      cur_words = cur_sentence.split(" ")

      prev_words_in_sentences = self.split_special_char(prev_words[tag_end_word])
      cur_words_in_sentences = self.split_special_char(cur_words[tag_end_word])
      prev_end_words_rhyme = self.split_special_char(prev_end_words_rhyme)

      if prev_end_words_rhyme == "":
          try:
              if not self.compare(prev_words_in_sentences, cur_words_in_sentences):
                  error_word = cur_words[tag_end_word]
                  self.add_masked_word(
                      word=error_word,
                      line=idx_next + 1,
                      position=tag_end_word + 1
                  )

          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

      if prev_end_words_rhyme != "":
          try:
            if not self.compare(prev_words_in_sentences, prev_end_words_rhyme):
                error_word = prev_words[tag_end_word]
                self.add_masked_word(
                    word=error_word,
                    line=idx + 1,
                    position=tag_end_word + 1
                )

          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

          try:
            if not self.compare(prev_end_words_rhyme, cur_words_in_sentences):
                error_word = cur_words[tag_end_word]
                self.add_masked_word(
                    word=error_word,
                    line=idx_next + 1,
                    position=tag_end_word + 1
                )

          except Exception as e:
              print(f"{e} + {cur_sentence}")
              pass

      prev_sentence = " ".join(prev_words)
      cur_sentence = " ".join(cur_words)

      return prev_sentence, cur_sentence, cur_words[-1]
  

  def check_ryhme_stanze_type_78(
      self,
      sentences: str,
      most_common_rhyme: Optional[str] = None
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
      length_sentences = len(sentences)
      # Let's check The first sentence 
      pos_end_word = 6
      print(f"self.rhymes_dict[most_common_rhyme[0]]: {self.rhymes_dict[most_common_rhyme[0]]}")
      first_word = sentences[0].split(" ")[pos_end_word]
      rhyme_first_word = self.split_word(first_word)
      if rhyme_first_word not in self.rhymes_dict[most_common_rhyme[0]]:
          self.add_masked_word(
              word=first_word,
              line=1,
              position=pos_end_word + 1
      )  

      for i in range(1, length_sentences, 2):
         end_word = sentences[i].split(" ")[pos_end_word]
         rhyme_end_word = self.split_word(end_word)
         print(f"end_word: {end_word}")
         print(f"rhyme_end_word: {rhyme_end_word}")
         if rhyme_end_word not in self.rhymes_dict[most_common_rhyme[0]]:
            self.add_masked_word(
                word=end_word,
                line=i + 1,
                position=pos_end_word + 1
            )

      return "\n".join(sentences)

  def check_rhyme_stanza_type_68(
      self,
      sentences: str,
      first_words: str,
      prev_end_words_rhyme: str,
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
        sentences[i], sentences[i+1], prev_end_words_rhyme =\
            self.check_rhyme_pair(sentences[i], sentences[i + 1], i, i + 1, tag, prev_end_words_rhyme)

      return "\n".join(sentences)

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

      if tag == "78":
        # Check the rhyme of the last word of the stanza
        pos_last_word = len(first_words) - 1
        rhyme_list = []
        rhyme_dict = {}
        rhyme_list.append(self.split_word(first_words[pos_last_word]))
        for i in range(1, len(sentences), 2):
           last_word = self.split_word(sentences[i].split(" ")[pos_last_word])
           last_word = self.split_special_char(last_word)
           rhyme_list.append(last_word)
        #    print(f"self.rhymes_dict[last_word]: {self.rhymes_dict[last_word]}")
           rhyme_dict[last_word] = self.rhymes_dict[last_word]
        frequency_rhyme = defaultdict(int)

        for rhyme in rhyme_list:
            matched = False 
            for key, value in rhyme_dict.items():
                if rhyme in value:
                    matched = True
                    frequency_rhyme[key] = frequency_rhyme.get(key, 0) + 1
                    break
            if not matched:
                frequency_rhyme[rhyme] = frequency_rhyme.get(rhyme, 0) + 1

        max_freq = max(frequency_rhyme.values())
        most_common_rhyme = [k for k, v in frequency_rhyme.items() if v == max_freq]
          
        res = self.check_ryhme_stanze_type_78(
            sentences,
            most_common_rhyme
        )
      elif tag == "68":
        res = self.check_rhyme_stanza_type_68(
            sentences,
            first_words,
            prev_end_words_rhyme,
            start_index,
            tag
        )
      else:
        pass


      return res


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

      for i in cur_tone_dict:
          if self.get_tone(words[i]) != cur_tone_dict[i]:
              self.add_masked_word(
                 word = words[i], 
                 line = row_sentence + 1, 
                 position = i + 1
              )
              words[i] = words[i] + "(E_T)"
          else:
            if self.get_tone(words[i]) == 'uneven':
              sentence_correct[i] = sentence_correct[i] + "(T)"
            elif self.get_tone(words[i]) == 'even':
              sentence_correct[i] = sentence_correct[i] + "(B)"

      return " ".join(words), " ".join(sentence_correct)


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
      ### the first Define for the tone of the first sentence is _ T _ B _ T _ _
      first_tone_default = [[0, 3, 4, 7], [1, 2, 5, 6]] ## ==> 7 ffile, 71 file
      first_sentence_words_1 = sentences[0].split(" ")[1]
      # Check even , uneven for a sentence
      if self.get_tone(first_sentence_words_1) == 'uneven':
        first_tone_default_sentence = first_tone_default
      elif self.get_tone(first_sentence_words_1) == 'even':
        first_tone_default_sentence = [first_tone_default[1], first_tone_default[0]]

      for i in range(len(sentences)):
          sentences[i], sentence_correct = self.check_tone_sentence(sentences[i], i, first_tone_default_sentence, tag)
          sentences_correct.append(sentence_correct)
      return "\n".join(sentences), "\n".join(sentences_correct)


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
      stanza = self.check_rhyme_stanza(stanza, tag) # Create and record error unstructured sentences
      stanza, sentences_correct_format = self.check_tone_stanza(stanza, tag)
      sentences_correct_format = stanza
      return stanza, sentences_correct_format

  def check_spelling_vietnamese(
      self,
      stanza: str,
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
      for line, sentence in enumerate(sentences):
          words = sentence.split(" ")
          words_out = []
          for pos, word in enumerate(words):
            first_char = word[0].lower()
            vietnamese_chars = self.dictionary_vi[first_char]
            if self.split_special_char(word.lower()) in vietnamese_chars:
              continue
            else:
              self.add_masked_word(
                 word = word, 
                 line = line + 1, 
                 position = pos + 1
              )
              word = word + "(E_S)"
              recommend_correct_format[word] = vietnamese_chars
            words_out.append(word)
          sentences_correct_format.append(" ".join(words_out))
      # print(sentences_correct_format)
      return "\n".join(sentences_correct_format), recommend_correct_format


  def calculate_stanza_score(
        self,
        stanza: str,
        tag: str,
        ):
      """
        A function to calculate score for the Stanza

        param sentence: stanza

        return: score  after checked by rule and calculated by formula that rhyme accounts for 70% score rate
          and 30% left for tone
      """

      stanza = self.preprocess_stanza(stanza)
      total_spelling_errors = 0

      sentences_correct_format = []
      recommend_correct_format = {}
      try:
        if tag != "00":
          stanza, sentences_correct_format = self.check_rule(stanza, tag)
        elif tag == "00":
          sentences_correct_format, recommend_correct_format = self.check_spelling_vietnamese(stanza, total_spelling_errors, sentences_correct_format, recommend_correct_format)

      except Exception as e:
          print(e)
          score = 0
          sentences_correct_format = ""
      return sentences_correct_format, recommend_correct_format


  def check_poem(self,
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

      sentences_correct_format = ""
      recommend_correct_format = {}
      for i in poem.split("\n\n"):
          sentences_correct_format, recommend_correct_format = self.calculate_stanza_score(i, tag)
          print(sentences_correct_format)
          print(recommend_correct_format)
      return self.idx_masked_words, self.masked_words 
  



if __name__ == "__main__":
    import os 
    # get the root path
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_path = os.path.dirname(os.path.dirname(root_path))
    # print(f"\n\n[ROOT_PATH]: {root_path} \n\n")
    full_path = os.path.join(root_path, sources)
    # print(f"\n\n[SOURCES]: {sources} \n\n")

    vowels_path = full_path + "start_vowels.txt"
    rhyme_path = full_path + "rhymes.txt"
    tone_path = full_path + "tone_dict.txt"
    special_tone_path = full_path + "vocab_dupple_check.txt"
    dictionary_path = full_path + "words.txt"

    check_poetic_rule = PoeticRules(
       vowels_dict_path = vowels_path, 
       rhyme_dict_path=rhyme_path, 
       tone_dict_path=tone_path, 
       dictionary_path=dictionary_path, 
       special_tone_dict_path=special_tone_path
    )
    luc_bat = True
    poem = ""
    if luc_bat:
        poem = "cởi trời xanh cởi đất nâu \ngió mấy hờn dỗi bạc na nhớ nhùng \nbạc đầu tóc trắng da nhé \ncõi lửa thế giới ai nhung lưng sầu \nnhớ quê hương thơ nhuộm sầu \ntóc thể vương vương đôi sánh vai tròn \nđêm buồn ngắm ánh trăng tròn \nngẩn ngơ ôm bóng mỏi tròn năm canh."
    else:
        poem = "Hoàng hôn tắt nắng phủ sương mờ \nbóng tối giăng đầy vạn nẻo sơi \nngọn cỏ thu sương lay khẽ khẽ \nđầu non điểm xuyết ánh lơ thơ \ncôn trùng rỉ rả nghe mà chán \ncon nhện buông tơ rối cả trơ \nlặng lẽ tìm con buồn héo hắt \nkhói sương lẩn khuất ánh lóe vàng."
    tags = "68" if luc_bat else "78"
    idx_masked_words, masked_words = check_poetic_rule.check_poem(poem, tag=tags)

    print(f"\n\n[IDX_MASKED_WORDS]: {idx_masked_words} \n")
    print(f"\n\n[MASKED_WORDS]: {masked_words} \n")  

    # python mtm/mtm/processes/poetic_rule.py  

# =========================  LỤC BÁT
# cởi trời xanh cởi đất nâu 
# \ngió MẤY hờn dỗi bạc nâu nhớ nhùng  | (2_2) - TONE, 
# \nbạc đầu tóc trắng da nhung 
# \ncõi LỬA thế giới ai nhung lưng sầu | (4_2) - TONE, 
# \nnhớ quê hương THƠ nhuộm sầu | (5_4) - TONE
# \ntóc THỂ vương VƯƠNG đôi SÁNH vai tròn | (6_2) - TONE, (6_4) - TONE, (6_6) - TONE, RHYME 
# \nđêm buồn ngắm ánh trăng tròn 
# \nngẩn ngơ ôm bóng mỏi tròn năm canh.


# =========================  THẤT NGÔN BÁT CÚ
# Hoàng hôn tắt nắng phủ sương mờ 
# bóng tối giăng đầy vạn nẻo sơi | (2_7) - RHYME
# ngọn cỏ thu sương lay khẽ khẽ 
# đầu non điểm xuyết ánh lơ thơ 
# côn trùng rỉ rả nghe mà chán 
# con nhện buông tơ rối cả trơ 
# lặng lẽ tìm con buồn héo hắt 
# khói sương lẩn khuất ánh LÓE VÀNG | (8_6) - TONE, (8_7) - RHYME



