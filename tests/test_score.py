import os 
import sys
import pytest 
# Add the project root to sys.path
# Assuming your project root is two levels up from this test file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root) # Insert at the beginning to prioritize

# print(f"CURRENT_ROOOT {current_dir}")
# print(f"PROJECT_ROOOT {project_root}")


from avp.avp.tools.poetic import _score

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
    check_running_calculate_score(
        poem, 
        luc_bat=luc_bat,
        targeted_score=95.00
    )

# if __name__ == "__main__":
#     poem = "cởi trời xanh cởi đất nâu\n gió mây hờn dỗi bạc nâu nhớ nhung\n bạc đầu tóc trắng da nhung\n cõi tình thế giới ai nhung lưng sầu\n nhớ quê hương nhớ nhuộm sầu\n tóc thề vương vấn đôi sầu vai tròn\n đêm buồn ngắm ánh trăng tròn\n ngẩn ngơ ôm bóng mỏi tròn năm canh. "
#     luc_bat = True
#     check_running_calculate_score(poem, luc_bat=luc_bat)
