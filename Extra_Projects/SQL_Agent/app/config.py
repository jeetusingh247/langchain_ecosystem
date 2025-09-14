import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self._load()

    def _load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                cfg = yaml.safe_load(f)
        else:
            cfg = {}
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", cfg.get("GEMINI_API_KEY", ""))
        self.LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", cfg.get("LANGCHAIN_API_KEY", ""))
        self.DB_URL = os.getenv("DB_URL", cfg.get("DB_URL", "sqlite:///./test.db"))

config = Config()
