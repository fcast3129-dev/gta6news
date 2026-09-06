import json, re
from openai import OpenAI
import config

def _extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    s, e = text.find("{"), text.rfind("}")
    if s == -1 or e == -1:
        raise ValueError("JSON IA introuvable")
    return json.loads(text[s:e+1])

def generate_video_plan():
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY manquante")

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    prompt = f"""
Crée un YouTube Short en {config.LANGUAGE} sur {config.NICHE}.
Durée cible : {config.TARGET_DURATION_SECONDS} secondes.
5 à 8 scènes. Accroche forte. N'invente jamais une actualité récente.
Chaque scène doit avoir des mots-clés visuels correspondant à des visuels officiels GTA VI.

Retourne uniquement ce JSON :
{{
  "topic":"sujet",
  "title":"titre",
  "description":"description",
  "hashtags":["#GTA6","#GTAVI","#shorts"],
  "voiceover":"voix off complète",
  "scenes":[
    {{"headline":"titre court","body":"phrase courte","visual_keywords":["Jason","Vice City"]}}
  ]
}}
"""
    r = client.responses.create(model=config.TEXT_MODEL, input=prompt)
    return _extract_json(r.output_text)
