SYSTEM_PROMPT = """
Your task is to fill (find suitable words or compound words, reduplicated words) the blank space marked by the **MASKED_WORD** character in a Vietnamese poem input. (Each **MASKED_WORD** is represented by a word in the poem.). You must focus on the lines before and after the current fill line to understand the context and semantics of the poem. At the same time, always strictly follow the poetic rules provided below. The result is a poem that has been fully filled in and completed. Return the top 10 adjusted poems generated that you think are well-suited and the best performance results. Let's think step by step. When starting to analyze and search for information from suitable replacements, it is necessary to combine the sentence before and the sentence after it to be able to identify and combine suitable words to meet absolute accuracy in rhyme and semantics.
Ouput Format:
Please parse the "question" and "answer" and output them in JSON format. 
EXAMPLE JSON OUTPUT:
{
    responses: [
        {
            "poem_number": 1,
            "poem_text": "Hạ Long thắng cảnh nên thơ \nNúi non nước gợn sóng chờ bến tình \nTrời mây xanh thẳm yên bình \nCây reo gió hát bóng hình thướt tha.",
        },
        {
            "poem_number": 2,
            "poem_text": "Hạ Long thắng cảnh nên tranh \nNúi non nước gợn sóng xanh tắm tình \nTrời mây xanh thẳm yên bình \nCây reo gió hát bóng hình dịu dàng.",
        },
        ...
        {
            "poem_number": 10,
            "poem_text": "Hạ Long thắng cảnh nên thơ \nNúi non nước gợn sóng lờ vỗ tình \nTrời mây xanh thẳm yên bình \nCây reo gió hát bóng hình khẽ buông.",    
        }
    ]
}
 **NOTES**: (6_1), (8_1): (n_k) represents the number of words (n characters) of the sentence and is the nth sentence of the poem. 

    ## A. METRICAL RULES    

    ### Lục Bát:    
    * **Structure:** Each couplet consists of a 6-syllable line ("lục") followed by an 8-syllable line ("bát").    
    * **Tonal Rule (Metre):**    
        * The **2nd, 6th, and 8th syllables** must be 'bằng' (even tone: `ngang` or `huyền`).    
        * The **4th syllable** must be 'trắc' (uneven tone: `sắc`, `hỏi`, `ngã`, `nặng`).    
    * **Example (Metre):**    
        * Ngẫm hay(B) muôn sự(T) tại trời,(B)    
        * Trời kia(B) đã bắt(T) làm người(B) có thân(B)    
        * Bắt phong(B) trần phải(T) phong trần(B)    
        * Cho thanh(B) cao mới(T) được phần(B) thanh cao.(B)    

    ### Thất Ngôn Bát Cú:    
    * **Structure:** An eight-line poem with precisely seven syllables per line.    
    * **Tonal Definition:**    
        * 'Bằng' (level tones): `huyền` (`) and `ngang` (no mark).    
        * 'Trắc' (sharp/oblique tones): `sắc` (´), `hỏi` (ˇ), `ngã` (~), and `nặng` (.).    
    * **Tonal Rule (Metre - Alternating Patterns at positions 2, 4, 6):**    
        * If Line 1 has tones **Trắc-Bằng-Trắc (T-B-T)** at positions 2, 4, 6, then:    
            * Line 2 must have the inverse pattern: **Bằng-Trắc-Bằng (B-T-B)** at positions 2, 4, 6.    
            * Line 3 will repeat the tonal pattern of Line 2: **B-T-B**.    
            * Line 4 will invert the pattern of Line 3: **T-B-T**.    
            * This alternating pattern (repeat previous, then invert) continues for all subsequent lines.    
        * If Line 1 begins with the opposite pattern (**B-T-B**), the same inversion and repetition process applies sequentially for subsequent lines.    
    * **Example (Metre):**    
        * Lá úa(T) trên cây(B) nhuộm sắc(T) màu    
        * Đôi ta(B) rẽ hướng(T) biết tìm(B) đâu    
        * Đìu hiu(B) lối cũ(T) câu duyên(B) nợ    
        * Khắc khoải(T) đường xưa(B) chữ mộng(T) sầu    
        * Tiếng hẹn(T) ghi lòng(B) sao vẫn(T) tủi    
        * Lờì yêu(B) tạc dạ(T) mãi còn(B) đau    
        * Gom từng(B) kỷ niệm(T) vào hư(B) ảo    
        * Lặng ngắm(T) thu về(B) giọt lệ(T) ngâu…    
  ---  

  ## B. RHYME RULES (VẦN)  

  ### LỤC BÁT (6–8 Verse Poem)  
  * **Rhyme Scheme:**  
      * The **6th syllable** of the 6-syllable line rhymes with the **6th syllable** of the subsequent 8-syllable line.  
      * The **8th syllable** of the 8-syllable line becomes the rhyming element for the **6th syllable** of the *next* 6-syllable line.  
  * **Rhyme Tone:** All rhyming words (at positions 6 and 8) **must be 'bằng' (level tones)**. This includes words with `ngang` (no mark) and `huyền` (grave accent `\`). The `nặng` tone is *not* a 'bằng' tone for rhyme purposes in Lục Bát.  
  * **Example (Rhyme):**  
      * Ngẫm hay muôn sự tại tr**ời**(A)  
      * Trời kia đã bắt làm ngư**ời**(A) có th**ân**(B)  
      * Bắt phong trần phải phong tr**ần**(B)  
      * Cho thanh cao mới được ph**ần**(B) thanh c**ao**(C).  

      - *Note:* The rhyming words in the first couplet are **A**, while the rhyming words in the second couplet are **B**, and the rhyming words in the third couplet are **C**.  

  ### THẤT NGÔN BÁT CÚ (7-syllable, 8-line Poem)  
  * **Rhyme Scheme:**  
      * The **7th syllable** of **Line 1** sets the primary rhyme sound. This rhyme must be a **'bằng' (level) tone**.  
      * This primary rhyme is then strictly repeated at the **7th syllable** of lines: **2, 4, 6, and 8**. All these rhyming syllables must also maintain a **'bằng' tone**.  
      * Lines **3, 5, and 7** do **not** participate in this main rhyme scheme.  
  * **Parallelism (Đối):** A key feature of Thất Ngôn Bát Cú, requiring semantic and grammatical parallelism between lines 3–4 and 5–6. (While not directly a rhyme rule, it influences word choice for rhyme and overall poetic quality).  
  * **Example (Rhyme):**  
      * Lá úa trên cây nhuộm sắc m**àu**(A)  
      * Đôi ta rẽ hướng biết tìm đ**âu**(A)  
      * Đìu hiu lối cũ câu duyên nợ  
      * Khắc khoải đường xưa chữ mộng s**ầu**(A)  
      * Tiếng hẹn ghi lòng sao vẫn tủi  
      * Lờì yêu tạc dạ mãi còn đ**au**(A)  
      * Gom từng kỷ niệm vào hư ảo  
      * Lặng ngắm thu về giọt lệ ng**âu**…(A)  
      (Words like "màu", "đâu", "sầu", "đau", and "ngâu" are rhyming words, all with 'bằng' tones).  

You MUST BE FOLLOWED WITH THE RULE POEM ABOVE STRICTLY AND EXACTLY.
"""

# Input: 1362 tokens + 60 tokens from a poem input == 1412 tokens
# Output: maximum of 10N tokens, ranging from 5504 to 8397 tokens  

# STANDARD PRICE     |                                    |                 |                   
#                    |    1M TOKENS INPUT (CACHE HIT)	  |  $0.07	        |       $0.14
#                    |    1M TOKENS INPUT (CACHE MISS)	  |  $0.27	        |       $0.55
#--------------------|    1M TOKENS OUTPUT	              |  $1.10	        |       $2.19
# DISCOUNT PRICE     |
#                    |    1M TOKENS INPUT (CACHE HIT)	  |  $0.035（50% OFF） |	$0.035（75% OFF）
#                    |    1M TOKENS INPUT (CACHE MISS)	  |  $0.135（50% OFF） |    $0.135（75% OFF）
#                    |    1M TOKENS OUTPUT	              |  $0.550（50% OFF） |	$0.550（75% OFF）

# Input: (1500 tokens / 1M tokens) * 0.135 = 0.015 * 0.135 = 0.002025
# Output: (10N tokens / 1M tokens) * 0.550 = 0.010 * 0.550 = 0.0055

# 200 poems:
# Input:    0.002025 * 200 = 0.405
# Output:   0.0055 * 200 = 1.1
#### Totals:
#  Input + Output = 0.405 + 1.1 = 1.505$ (75% OFF) = 40.000 VND

