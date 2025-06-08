from mtm.mtm.configs import CountSyllablePoemsConfig

class CountSyllablePoems:
    def __init__(self, config: CountSyllablePoemsConfig):
        super(CountSyllablePoems, self).__init__()
        # Lacking word, Reductant word 
        # self.masked_words = [
        #     #  {
        #     #     "line": 1,
        #     #     "position": 9,
        #     #     "word": None (don't masked) (because of reductant word,only delete it)
        #     #  },
        #     #  {
        #     #     "line": 2,
        #     #     "position": 8,
        #     #     "word": "missing"
        #     #  },
        # ]
        self.masked_words = config.masked_words
        self.idx_masked_words = config.idx_masked_words
        self.token_masked_words = config.token_masked_words

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

        self.idx_masked_words.add(f"{line}_{position}")

        print(f"Masked word: {word} at line {line}, position {position}")

    def check_poem_68(
            self,
            sentences: str,
    ):
        first_count = 6
        second_count = 8
        for line, sentence in enumerate(sentences):
            count_sentence = len(sentence.strip().split(" "))
            print(f'sentence: {sentence.strip().split(" ")}')
            print(f"count_sentence: {count_sentence}")
            if line % 2 == 0: 
                # reductant word
                if count_sentence > first_count:
                    self.add_masked_word(
                        word = "reductant" , 
                        line= line + 1,
                        position = first_count + 1
                    )
                # missing word
                elif count_sentence < first_count:
                    self.add_masked_word(
                        word = "missing", 
                        line= line + 1,
                        position = first_count
                    )
            else:
                if count_sentence > second_count:
                    self.add_masked_word(
                        word = "reductant", 
                        line= line + 1,
                        position = second_count + 1
                    )
                elif count_sentence < second_count:
                    self.add_masked_word(
                        word = "missing", 
                        line= line + 1,
                        position = second_count
                    )
                
        print(f"Completed successfully for checking LỤC BÁT poem")
    
    def check_poem_78(
            self,
            sentences: str,
    ):
        first_count = 7
        for line, sentence in enumerate(sentences):
            count_sentence = len(sentence.strip().split(" ")) 
            # reductant word
            if count_sentence > first_count:
                self.add_masked_word(
                    word = "reductant" , 
                    line= line + 1,
                    position = first_count + 1
                )
            # missing word
            elif count_sentence < first_count:
                self.add_masked_word(
                    word = "missing",
                    line= line + 1,
                    position = first_count 
                )

        print(f"Completed successfully for checking THẤT NGÔN BÁT CÚ poem")

         
    def count_syllables(
            self,
            stanza: str,
            luc_bat: bool
    ):
        """
            This is a function to check the count syllables of a stanza input before completing mask token processing

            Args:
                stanza: stanza to check

            Returns:
                idx_masked_words: index of masked words
                masked_words: list of masked words

        """
        sentences = stanza.split("\n")
        if luc_bat:
            self.check_poem_68(sentences)
        else:
            self.check_poem_78(sentences)

        return self.idx_masked_words, self.masked_words
    

if __name__ == "__main__":
    count_syllable_poems = CountSyllablePoems(
        config = CountSyllablePoemsConfig(
            masked_words = [],
            idx_masked_words = set(),
            token_masked_words = "MASKED_WORD"
        )
    )
    luc_bat = False
    if luc_bat:
        # #### LỤC BÁT ####
        # Lack 1 word in stanza 
        poem = "cởi trời xanh cởi đất \ngió mấy hờn dỗi bạc na nhớ \nbạc đầu tóc trắng da nhé \ncõi lửa thế giới ai nhung lưng sầu \nnhớ quê hương thơ nhuộm sầu \ntóc thể vương vương đôi sánh vai tròn \nđêm buồn ngắm ánh trăng tròn \nngẩn ngơ ôm bóng mỏi tròn năm canh."
        # Reduct 1 word in stanza
        poem_1 = "cởi trời xanh cởi đất nâu nâu \ngió mấy hờn dỗi bạc na nhớ nhùng nâu \nbạc đầu tóc trắng da nhé \ncõi lửa thế giới ai nhung lưng sầu \nnhớ quê hương thơ nhuộm sầu \ntóc thể vương vương đôi sánh vai tròn \nđêm buồn ngắm ánh trăng tròn \nngẩn ngơ ôm bóng mỏi tròn năm canh."
    else:
        # #### THẤT NGÔN BÁT CÚ ####
        # Lack 1 word in stanza
        poem = "Hoàng hôn tắt nắng phủ sương \nbóng tối giăng đầy vạn nẻo sơi \nngọn cỏ thu sương lay khẽ khẽ \nđầu non điểm xuyết ánh lơ thơ \ncôn trùng rỉ rả nghe mà chán \ncon nhện buông tơ rối cả trơ \nlặng lẽ tìm con buồn héo hắt \nkhói sương lẩn khuất ánh lóe vàng."
        poem_1 = "Hoàng hôn tắt nắng phủ sương mờ mờ \nbóng tối giăng đầy vạn nẻo sơi \nngọn cỏ thu sương lay khẽ khẽ \nđầu non điểm xuyết ánh lơ thơ \ncôn trùng rỉ rả nghe mà chán \ncon nhện buông tơ rối cả trơ \nlặng lẽ tìm con buồn héo hắt \nkhói sương lẩn khuất ánh lóe vàng."

    idx_masked_words, masked_words = count_syllable_poems.count_syllables(
        stanza = poem_1,
        luc_bat = luc_bat
    )

    print(f"idx_masked_words: {idx_masked_words}")
    print(f"masked_words: {masked_words}")



# "cởi trời xanh cởi đất 
# \ngió mấy hờn dỗi bạc na nhớ nhùng 
# \nbạc đầu tóc trắng da nhé 
# \ncõi lửa thế giới ai nhung lưng sầu 
# \nnhớ quê hương thơ nhuộm sầu 
# \ntóc thể vương vương đôi sánh vai tròn 
# \nđêm buồn ngắm ánh trăng tròn 
# \nngẩn ngơ ôm bóng mỏi tròn năm canh."