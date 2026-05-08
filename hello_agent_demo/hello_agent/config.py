import os

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY", "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"
)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "123")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "Qwen/Qwen3.5-35B-A3B-FP8")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://10.12.2.102:8101/v1")
