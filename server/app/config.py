import os
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-default-openai-key")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
GOOGLE_CLOUD_TTS_CREDENTIALS_PATH = os.getenv("GOOGLE_CLOUD_TTS_CREDENTIALS_PATH", "secrets/google-credentials.json")

# TTS Configuration
#TTS_PROVIDER = os.getenv("TTS_PROVIDER", "gTTS")  # or "GoogleCloudTTS"
TTS_PATH = os.getenv("TTS_PATH", "app/storage/tts")

TTS_PROVIDER="GoogleCloudTTS"
GOOGLE_CLOUD_TTS_CREDENTIALS_PATH="secrets/google-credentials.json"
# System Config
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"