from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    secret_file = Path(config.YOUTUBE_CLIENT_SECRET_FILE)

    if not secret_file.exists():
        raise SystemExit(
            f"Fichier OAuth absent : {secret_file}\n"
            "Télécharge les identifiants OAuth Google et place-les sous ce nom."
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(secret_file),
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    Path(config.YOUTUBE_TOKEN_FILE).write_text(
        creds.to_json(),
        encoding="utf-8"
    )

    print(f"Autorisation réussie : {config.YOUTUBE_TOKEN_FILE}")

if __name__ == "__main__":
    main()
