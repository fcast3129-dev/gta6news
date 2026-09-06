import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
NICHE = os.getenv("NICHE", "GTA 6")
LANGUAGE = os.getenv("LANGUAGE", "français")
TARGET_DURATION_SECONDS = int(os.getenv("TARGET_DURATION_SECONDS", "40"))

TEXT_MODEL = os.getenv("TEXT_MODEL", "gpt-5")
TTS_MODEL = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("TTS_VOICE", "alloy")

AUTO_PUBLISH = os.getenv("AUTO_PUBLISH", "false").lower() == "true"

YOUTUBE_PRIVACY = os.getenv("YOUTUBE_PRIVACY", "private")
YOUTUBE_CATEGORY_ID = os.getenv("YOUTUBE_CATEGORY_ID", "24")
YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")

VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
FPS = int(os.getenv("FPS", "30"))

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
