"""
config.py - Settings of the project.
This file loads the secret API key from the .env file.
NEVER write your API key directly inside the code. Always keep it in .env.
"""

import os
from dotenv import load_dotenv

# Folder where this file lives (so .env is always found)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# --- Secret key (read from .env file) ---
ZAI_API_KEY = os.getenv("ZAI_API_KEY", "")

# --- AI model name. glm-5.3-flash is fast and low cost. ---
# You can change it in the .env file (example: glm-5.3)
ZAI_MODEL = os.getenv("ZAI_MODEL", "glm-5.3-flash")

# --- Z.ai GLM API address (OpenAI-compatible chat endpoint) ---
ZAI_API_URL = "https://api.z.ai/api/paas/v4/chat/completions"

# --- Assistant name used everywhere in the app ---
ASSISTANT_NAME = "Nova"

# --- Speaking speed in words per minute (140 slow - 200 fast) ---
VOICE_RATE = 170


def check_api_key():
    """Return True if the API key looks correctly set."""
    if not ZAI_API_KEY or "your_api_key_here" in ZAI_API_KEY:
        return False
    return True
