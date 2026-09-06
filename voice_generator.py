from pathlib import Path
from openai import OpenAI
import config

def generate_voice(text: str, output_path: Path) -> Path:
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY manquante dans .env")

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with client.audio.speech.with_streaming_response.create(
        model=config.TTS_MODEL,
        voice=config.TTS_VOICE,
        input=text,
        instructions="Voix française naturelle, énergique, claire, rythme de vidéo courte."
    ) as response:
        response.stream_to_file(output_path)

    return output_path
