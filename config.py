import os

from dotenv import load_dotenv


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE)) 


load_dotenv(os.path.join(ROOT, ".env"))


MODEL_NAME = os.getenv("MODEL_NAME", "qwen-plus")
BASE_URL = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
API_KEY = os.getenv("DASHSCOPE_API_KEY") 

DB = os.getenv("DB", os.path.join(ROOT, "data", "blastdb", "demo_proteins"))


EVALUE = float(os.getenv("EVALUE", "1e-3"))
MAX_HITS = int(os.getenv("MAX_HITS", "5"))
