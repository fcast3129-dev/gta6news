from datetime import datetime
import json
import re

import config
from ai_generator import generate_video_plan
from voice_generator import generate_voice
from video_builder import build_video

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60] or "video"

def main():
    print("1/4 Génération du concept et du script...")
    plan = generate_video_plan()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = config.OUTPUT_DIR / f"{stamp}_{slugify(plan['topic'])}"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("2/4 Génération de la voix...")
    audio_path = run_dir / "voice.mp3"
    generate_voice(plan["voiceover"], audio_path)

    print("3/4 Création de la vidéo...")
    video_path = run_dir / "short.mp4"
    build_video(plan, audio_path, video_path)

    print(f"Vidéo créée : {video_path}")

    if config.AUTO_PUBLISH:
        print("4/4 Upload YouTube...")
        from youtube_uploader import upload_video
        response = upload_video(video_path, plan)
        print("Upload terminé.")
        print("YouTube video ID :", response.get("id"))
    else:
        print("4/4 Publication désactivée : AUTO_PUBLISH=false")
        print("Vérifie d'abord la vidéo avant d'activer l'upload.")

if __name__ == "__main__":
    main()
