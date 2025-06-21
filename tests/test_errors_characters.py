import re
if __name__ == "__main__":
    # Define valid Vietnamese letters and characters
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

    # Input poem
    text = "con xin một trái nha ông \ncủa nhà còn ít nhưng không muốn thừa \nnhìn ông lúc nắng lúc mưa \nđi đâu bà cũng sớm trưa bên mình \nmột thời vất vả mưu sinh \nnh℉ vui có bóng hình bên ta \ngiờ đây tóc bạc trắng ngà \nbà đi để lại căn nhà vắng tanh"
    print(text)
    def mask_invalid_characters(text, allowed_chars, mask="[MASKED_TOKEN]"):
        new_lines = []
        for line in text.strip().split("\n"):
            new_line = ""
            for ch in line:
                if ch not in allowed_chars:
                    new_line = mask
                else:
                    new_line += ch
            new_lines.append(new_line)
        return "\n".join(new_lines)

    # Apply masking
    masked_text = mask_invalid_characters(text, allowed_chars)

    # Output
    print(masked_text)
