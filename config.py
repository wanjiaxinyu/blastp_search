"""Stage 3 的配置。相比 Stage 2,把写死的设置集中到这里,并支持用 .env 覆盖。

⚠️ 这里有个很容易踩的坑(之前就踩过):必须【先加载 .env,再读环境变量】。
下面的 os.getenv 是在 import 本文件时就执行的,所以 load_dotenv 一定要在它们【之前】调用,
否则会出现"明明在 .env 里配了,程序却还用默认值"的诡异现象。
我们显式传入项目根目录的 .env 路径,这样不管从哪个目录运行都能找到。
"""

import os

from dotenv import load_dotenv

# 项目根目录 = 本文件(在 stage3_agent_config 下)的上两级
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # MCP 目录深一层,多上跳一级到仓库根

# 关键:先加载根目录的 .env,再读下面的环境变量
load_dotenv(os.path.join(ROOT, ".env"))

# 千问(阿里云百炼)配置。都可以在 .env 里覆盖。
MODEL_NAME = os.getenv("MODEL_NAME", "qwen-plus")
BASE_URL = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
API_KEY = os.getenv("DASHSCOPE_API_KEY")   # 在 .env 里填:DASHSCOPE_API_KEY=sk-xxx

# 数据库路径
DB = os.getenv("DB", os.path.join(ROOT, "data", "blastdb", "demo_proteins"))

# BLAST 默认参数
EVALUE = float(os.getenv("EVALUE", "1e-3"))
MAX_HITS = int(os.getenv("MAX_HITS", "5"))
