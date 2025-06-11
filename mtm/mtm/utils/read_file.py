import os 
import pandas as pd 

from mtm.mtm.configs import *


# Read Excel File (Google Sheets from url)
def read_file(
        file_path: str,
        is_url: bool = False
) -> str:
    if is_url:
        print(f"[DATA FROM GOOGLE SHEETS]: Reading successful")
        data = pd.read_csv(file_path)
        return data
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f"[DATA FROM FILE]: Reading successful")
        return f.read()

def read_file_from_url(url: str) -> str:
    is_url = False
    sheet_id = None
    grid = None
    base_url = url
    if url.startswith("http://") or url.startswith("https://"):
        is_url = True
    
        # Get sheet id from url
        if url.startswith("https://docs.google.com/spreadsheets/d/"):
            sheet_id = url.split("d/")[1].split("/")[0]
        else:
            sheet_id = url.split("spreadsheets/d/")[1].split("/")[0]
        
        grid = url.split("gid=")[1].replace("#", "")

    if sheet_id is None:
        raise Exception("Invalid url")
    
    print(f"sheet_id: {sheet_id}")
    print(f"grid: {grid}")

    if is_url:
        base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={grid}"

    return read_file(
        file_path=base_url,
        is_url=is_url
    )


if __name__ == "__main__":
    test = read_file_from_url(GOOGLE_SHEETS_URL)
    print(f"test: {test}")

