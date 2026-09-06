from pathlib import Path
from openai import OpenAI
import config

def generate_voice(text: str, output_path: Path):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    with client.audio.speech.with_streaming_response.create(
        model=config.TTS_MODEL,
        voice=config.TTS_VOICE,
        input=text,
        instructions="Voix française naturelle, énergique et claire."
    ) as response:
        response.stream_to_file(output_path)
    return output_path
