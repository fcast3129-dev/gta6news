# Video Auto Bot — Starter Pack

Bot Python pour créer automatiquement des vidéos verticales 1080x1920 avec :
- sujet + script générés par IA
- voix IA
- slides verticales
- texte/sous-titres intégrés
- export MP4
- upload YouTube optionnel
- mode test par défaut

## IMPORTANT

Par défaut :

```env
AUTO_PUBLISH=false
YOUTUBE_PRIVACY=private
```

Le bot crée donc la vidéo sans la publier.

## Installation

```bash
pip install -r requirements.txt
```

Copier `.env.example` vers `.env`, puis renseigner :

```env
OPENAI_API_KEY=...
```

Créer une vidéo :

```bash
python main.py
```

La vidéo apparaît dans `output/`.

## Choisir une niche

Dans `.env` :

```env
NICHE=GTA 6
```

Exemples : GTA 6, automobile, crypto, technologie, faits insolites, animaux, histoire.

## Préparer YouTube

1. Créer un projet Google Cloud.
2. Activer YouTube Data API v3.
3. Créer des identifiants OAuth 2.0.
4. Télécharger le JSON.
5. Le placer dans le dossier sous `client_secret.json`.
6. Lancer :

```bash
python youtube_auth.py
```

Cela crée `token.json`.

Ensuite seulement :

```env
AUTO_PUBLISH=true
YOUTUBE_PRIVACY=private
```

Commencer en privé.

## Hébergement

Le pack fonctionne sur un hébergeur supportant Python + FFmpeg.
Un `Dockerfile` est fourni.

## Version actuelle

Cette version privilégie la fiabilité :
- génération IA du concept
- voix IA
- plusieurs slides verticales
- montage MP4
- upload YouTube optionnel

Extensions possibles ensuite :
- images IA par scène
- B-roll vidéo
- tendances automatiques
- TikTok
- Instagram Reels
- publication planifiée
- analyse des performances
