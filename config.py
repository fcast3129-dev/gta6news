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
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
FPS = int(os.getenv("FPS", "30"))
IMAGE_COUNT = int(os.getenv("IMAGE_COUNT", "8"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
