from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
import textwrap
import shutil
import config

def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()

def _wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))

def create_slide(headline: str, body: str, index: int, total: int, out: Path):
    w, h = config.VIDEO_WIDTH, config.VIDEO_HEIGHT
    img = Image.new("RGB", (w, h), (18, 18, 24))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((70, 110, w - 70, 240), radius=30, fill=(42, 42, 55))
    draw.rounded_rectangle((70, h - 250, w - 70, h - 120), radius=30, fill=(32, 32, 43))

    title_font = _font(78, bold=True)
    body_font = _font(50, bold=False)
    small_font = _font(34, bold=True)

    headline_wrapped = _wrap(headline.upper(), 18)
    body_wrapped = _wrap(body, 28)

    draw.multiline_text(
        (w / 2, 650),
        headline_wrapped,
        font=title_font,
        anchor="mm",
        align="center",
        spacing=18
    )

    draw.multiline_text(
        (w / 2, 1050),
        body_wrapped,
        font=body_font,
        anchor="mm",
        align="center",
        spacing=16
    )

    draw.text((w / 2, 175), "VIDEO AUTO BOT", font=small_font, anchor="mm")
    draw.text((w / 2, h - 185), f"{index}/{total}", font=small_font, anchor="mm")

    img.save(out, quality=95)

def _audio_duration(audio_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

def build_video(plan: dict, audio_path: Path, output_path: Path) -> Path:
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("FFmpeg/ffprobe n'est pas installé.")

    work = output_path.parent / (output_path.stem + "_work")
    work.mkdir(parents=True, exist_ok=True)

    scenes = plan["scenes"]
    total = len(scenes)
    duration = _audio_duration(audio_path)
    per_scene = max(duration / total, 1.0)

    slide_paths = []
    for i, scene in enumerate(scenes, start=1):
        slide = work / f"slide_{i:02d}.png"
        create_slide(
            str(scene.get("headline", "")),
            str(scene.get("body", "")),
            i,
            total,
            slide
        )
        slide_paths.append(slide)

    concat_file = work / "slides.txt"
    with concat_file.open("w", encoding="utf-8") as f:
        for slide in slide_paths:
            f.write(f"file '{slide.resolve().as_posix()}'\n")
            f.write(f"duration {per_scene:.3f}\n")
        f.write(f"file '{slide_paths[-1].resolve().as_posix()}'\n")

    silent_video = work / "silent.mp4"

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-vf", f"scale={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT},format=yuv420p",
        "-r", str(config.FPS),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(silent_video)
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(silent_video),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ], check=True)

    return output_path
