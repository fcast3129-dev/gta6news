from pathlib import Path
from urllib.parse import urljoin
from io import BytesIO
import html, re, requests
from bs4 import BeautifulSoup
from PIL import Image

ROCKSTAR_PAGES = [
    "https://www.rockstargames.com/VI/media/screenshots",
    "https://www.rockstargames.com/VI/media",
    "https://www.rockstargames.com/VI",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

def _extract_urls(page_url, text):
    soup = BeautifulSoup(text, "html.parser")
    found = []

    for tag in soup.find_all(["img", "source"]):
        for attr in ("src", "data-src", "data-lazy-src"):
            v = tag.get(attr)
            if v:
                found.append(urljoin(page_url, html.unescape(v)))
        for attr in ("srcset", "data-srcset"):
            v = tag.get(attr)
            if v:
                for item in v.split(","):
                    u = item.strip().split(" ")[0]
                    if u:
                        found.append(urljoin(page_url, html.unescape(u)))

    for raw in re.findall(r'https?:\\?/\\?/[^\s"\'<>]+?\\.(?:jpg|jpeg|png|webp)(?:\\?[^\s"\'<>]*)?', text, re.I):
        found.append(raw.replace("\\/", "/"))

    unique = []
    seen = set()
    for u in found:
        if not u.startswith("http"):
            continue
        if any(x in u.lower() for x in ("logo","icon","favicon","esrb","playstation","xbox","sprite")):
            continue
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique

def discover_official_images():
    session = requests.Session()
    session.headers.update(HEADERS)
    all_urls = []
    for page in ROCKSTAR_PAGES:
        r = session.get(page, timeout=30)
        r.raise_for_status()
        all_urls.extend(_extract_urls(page, r.text))
    return list(dict.fromkeys(all_urls))

def _valid_image(content):
    try:
        with Image.open(BytesIO(content)) as im:
            w, h = im.size
            return w >= 700 and h >= 400
    except Exception:
        return False

def download_official_images(output_dir="downloaded_images", count=8):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for p in out.iterdir():
        if p.is_file():
            p.unlink()

    urls = discover_official_images()
    if not urls:
        raise RuntimeError("Aucune image détectée sur les pages Rockstar.")

    session = requests.Session()
    session.headers.update(HEADERS)
    saved = []

    for url in urls:
        if len(saved) >= count:
            break
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            if not _valid_image(r.content):
                continue
            with Image.open(BytesIO(r.content)) as im:
                im = im.convert("RGB")
                p = out / f"rockstar_{len(saved)+1:02d}.jpg"
                im.save(p, "JPEG", quality=92)
                saved.append(p)
        except Exception:
            pass

    if len(saved) < 2:
        raise RuntimeError("Pas assez d'images officielles téléchargées.")
    return saved
