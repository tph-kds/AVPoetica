import os 
import pytest 

from avp.avp.tools import _score

def check_running_calculate_score(
    poem: str,
    luc_bat: str,
    targeted_score: float,
):
    score = _score(poem, luc_bat)
    print(f"[TESTING CALCUALATING SCORE FROM WORKPROCESSING FOLDER] Score: {score}%")

    assert score >= targeted_score


def test_calculate_score():
    poem = "cởi trời xanh cởi đất nâu\n gió mây hờn dỗi bạc nâu nhớ nhung\n bạc đầu tóc trắng da nhung\n cõi tình thế giới ai nhung lưng sầu\n nhớ quê hương nhớ nhuộm sầu\n tóc thề vương vấn đôi sầu vai tròn\n đêm buồn ngắm ánh trăng tròn\n ngẩn ngơ ôm bóng mỏi tròn năm canh. "
    luc_bat = True
    check_running_calculate_score(poem, luc_bat=luc_bat)

# if __name__ == "__main__":
#     poem = "cởi trời xanh cởi đất nâu\n gió mây hờn dỗi bạc nâu nhớ nhung\n bạc đầu tóc trắng da nhung\n cõi tình thế giới ai nhung lưng sầu\n nhớ quê hương nhớ nhuộm sầu\n tóc thề vương vấn đôi sầu vai tròn\n đêm buồn ngắm ánh trăng tròn\n ngẩn ngơ ôm bóng mỏi tròn năm canh. "
#     luc_bat = True
#     check_running_calculate_score(poem, luc_bat=luc_bat)
