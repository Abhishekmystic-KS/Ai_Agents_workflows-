import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip().strip("'\"")

# Agent/Model Configurations
# Using gemini-2.5-flash as default (fast and supports tool calling)
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))

# Agent Loop Limits
MAX_STEPS = int(os.getenv("MAX_STEPS", "5"))
