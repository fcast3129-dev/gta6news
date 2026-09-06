from datetime import datetime
import json, re
import config
from ai_generator import generate_video_plan
from rockstar_images import download_official_images
from voice_generator import generate_voice
from video_builder import build_video

def slugify(text):
    return re.sub(r"[^a-z0-9]+","-",text.lower()).strip("-")[:60] or "video"

def main():
    print("1/5 Script...")
    plan = generate_video_plan()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = config.OUTPUT_DIR / f"{stamp}_{slugify(plan['topic'])}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir/"plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")

    print("2/5 Images officielles Rockstar...")
    imgs = download_official_images(count=config.IMAGE_COUNT)
    print(f"{len(imgs)} images téléchargées")

    print("3/5 Voix...")
    audio = run_dir/"voice.mp3"
    generate_voice(plan["voiceover"], audio)

    print("4/5 Montage...")
    video = run_dir/"short.mp4"
    build_video(plan, audio, video)

    print("5/5 Terminé :", video)
    print("Publication auto :", config.AUTO_PUBLISH)

if __name__ == "__main__":
    main()
