if __name__ == "__main__":

    text = """{
        "responses": [
            {
                "poem_number": 1,
                "poem_text": "câu thơ quên mất lối về\ntrăng khuya ẩn hiện mải mê trên đường\ntrách sao lời gió vấn vương\nngập ngừng chân bước như dường đam mê\nbóng cây nghiêng ngả ven lề\nvầng trăng gác tím u mê chẳng rời\nđêm nay đêm nữa đêm ơi\nthuyền trôi vô định không nơi bến bờ"
            },
            {
                "poem_number": 2,
                "poem_text": "câu thơ quên mất lối về\ntrăng khuya ẩn hiện mải mê trên đường\ntrách sao lời gió vấn vương\nngập ngừng chân bước như dường đam mê\nbóng cây nghiêng ngả ven lề\nvầng trăng gác say u mê chẳng rời\nđêm nay đêm nữa đêm ơi\nthuyền trôi vô định không nơi bến bờ"
            },
            {
                "poem_number": 3,
                "poem_text": "câu thơ quên mất lối về\ntrăng khuya ẩn hiện mải mê trên đường\ntrách sao lời gió vấn vương\nngập ngừng chân bước như dường đam mê\nbóng cây nghiêng ngả ven lề\nvầng trăng gác lụa u mê chẳng rời\nđêm nay đêm nữa đêm ơi\nthuyền trôi vô định không nơi bến bờ"
            },
            {
                "poem_number": 4,
                "poem_text": "câu thơ quên mất lối về\ntrăng khuya ẩn hiện mải mê trên đường\ntrách sao lời gió vấn vương\nngập ngừng chân bước như dường đam mê\nbóng cây nghiêng ngả ven lề\nvầng trăng gác xa u mê chẳng rời\nđêm nay đêm nữa đêm ơi\nthuyền trôi vô định không nơi bến bờ"
            },
            {
                "poem_number": 5,
                "poem_text": "câu thơ quên mất lối về\ntrăng khuya ẩn hiện mải mê trên đường\ntrách sao lời gió vấn vương\nngập ngừng chân bước như dường đam mê\nbóng cây nghiêng ngả ven lề\nvầng trăng gác thiều u mê chẳng rời\nđêm nay đêm nữa đêm ơi\nthuyền trôi vô định không nơi bến bờ"
            }
        ]
    }"""

    if not (
        (text.strip().startswith("{") and text.strip().endswith("}")) or
        (text.strip().startswith("```json") and text.strip().endswith("```"))
    ):
        print('{"error_msg": "Not having json format. Something went wrong. Please try again."}')
    else:
        print(f"Text: \n{text}")