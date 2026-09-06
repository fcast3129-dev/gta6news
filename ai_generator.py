import json
import re
from openai import OpenAI
import config

def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\\s*", "", text)
        text = re.sub(r"\\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("La réponse IA ne contient pas de JSON valide.")

    return json.loads(text[start:end + 1])

def generate_video_plan() -> dict:
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY manquante dans .env")

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    prompt = f"""
Tu es un producteur de vidéos verticales très courtes.

Crée UNE idée de vidéo pour la niche : {config.NICHE}.
Langue : {config.LANGUAGE}.
Durée cible : environ {config.TARGET_DURATION_SECONDS} secondes.

Contraintes :
- accroche dès la première phrase
- ton dynamique
- 5 à 8 scènes
- phrases courtes
- adapté à YouTube Shorts
- ne jamais inventer une actualité comme si elle était vraie
- si le sujet dépend d'une actualité récente non fournie, faire un contenu intemporel

Retourne uniquement du JSON valide :

{{
  "topic": "sujet",
  "title": "titre YouTube",
  "description": "description courte",
  "hashtags": ["#shorts", "#exemple"],
  "voiceover": "texte complet de la voix off",
  "scenes": [
    {{
      "headline": "texte court affiché",
      "body": "une ou deux lignes"
    }}
  ]
}}
"""

    response = client.responses.create(
        model=config.TEXT_MODEL,
        input=prompt
    )

    data = _extract_json(response.output_text)

    for key in ["topic", "title", "description", "hashtags", "voiceover", "scenes"]:
        if key not in data:
            raise ValueError(f"Champ manquant : {key}")

    if not isinstance(data["scenes"], list) or len(data["scenes"]) < 2:
        raise ValueError("Le plan doit contenir au moins 2 scènes.")

    return data
