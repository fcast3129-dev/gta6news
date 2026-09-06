from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_path: Path, plan: dict):
    token_file = Path(config.YOUTUBE_TOKEN_FILE)

    if not token_file.exists():
        raise RuntimeError("token.json absent. Lance d'abord : python youtube_auth.py")

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    youtube = build("youtube", "v3", credentials=creds)

    tags = [h.lstrip("#") for h in plan.get("hashtags", [])]

    body = {
        "snippet": {
            "title": plan["title"][:100],
            "description": (
                plan.get("description", "")
                + "\n\n"
                + " ".join(plan.get("hashtags", []))
            )[:5000],
            "tags": tags[:30],
            "categoryId": config.YOUTUBE_CATEGORY_ID,
        },
        "status": {
            "privacyStatus": config.YOUTUBE_PRIVACY,
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(
        str(video_path),
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    return request.execute()
