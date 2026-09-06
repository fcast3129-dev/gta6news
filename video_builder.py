from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess, textwrap, shutil
import config

def _font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

def _wrap(text, width):
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=False))

def _audio_duration(audio_path):
    r = subprocess.run([
        "ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(audio_path)
    ], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())

def create_slide(scene, bg_path, index, total, out):
    w,h = config.VIDEO_WIDTH, config.VIDEO_HEIGHT
    img = Image.open(bg_path).convert("RGB")
    img = ImageOps.fit(img, (w,h), method=Image.Resampling.LANCZOS)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, Image.new("RGBA",(w,h),(0,0,0,65)))

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((45,1320,w-45,1770), radius=30, fill=(0,0,0,150))
    draw.multiline_text(
        (w/2,1390), _wrap(scene.get("headline",""),19),
        font=_font(72,True), anchor="ma", align="center", fill="white", spacing=10
    )
    draw.multiline_text(
        (w/2,1580), _wrap(scene.get("body",""),30),
        font=_font(44), anchor="ma", align="center", fill="white", spacing=10
    )
    draw.text((w-65,h-65), f"{index}/{total}", font=_font(30,True), anchor="rs", fill="white")
    img.convert("RGB").save(out, "JPEG", quality=94)

def build_video(plan, audio_path, output_path):
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg absent")

    work = output_path.parent / "short_work"
    work.mkdir(parents=True, exist_ok=True)
    bgs = sorted(Path("downloaded_images").glob("*.jpg"))
    scenes = plan["scenes"]
    duration = _audio_duration(audio_path)
    per_scene = max(duration/len(scenes), 1.0)

    slides=[]
    for i, scene in enumerate(scenes, start=1):
        p = work / f"slide_{i:02d}.jpg"
        create_slide(scene, bgs[(i-1)%len(bgs)], i, len(scenes), p)
        slides.append(p)

    concat = work/"slides.txt"
    with concat.open("w", encoding="utf-8") as f:
        for p in slides:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            f.write(f"duration {per_scene:.3f}\n")
        f.write(f"file '{slides[-1].resolve().as_posix()}'\n")

    silent = work/"silent.mp4"
    subprocess.run([
        "ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),
        "-vf",f"scale={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT},format=yuv420p",
        "-r",str(config.FPS),"-c:v","libx264","-pix_fmt","yuv420p",str(silent)
    ], check=True)

    subprocess.run([
        "ffmpeg","-y","-i",str(silent),"-i",str(audio_path),
        "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(output_path)
    ], check=True)

    return output_path
