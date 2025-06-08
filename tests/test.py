import os 
import pytest 

def check_source_path(check_path: str):
    sources = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n\n[TESTING]: {check_path} ... \n\n")
    assert sources == check_path


def test_source_path():
    check_source_path(r"D:\DataScience_For_mySelf\Graduation_thesis\AVPoetica")

    # pytest tests/test_score.py -s -v
