import os
import sys 
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
