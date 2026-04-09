# Uppgiftslösare

Ladda upp .txt-filer och få svar på uppgifter via AI. Svaren kan laddas ner som .txt.

## Deploya på Railway (gratis, enklast)

1. Skapa konto på https://railway.app
2. Klicka "New Project" → "Deploy from GitHub repo"
   - Ladda upp den här mappen till ett GitHub-repo först (github.com → New repository)
3. Lägg till miljövariabel i Railway:
   - Gå till ditt projekt → Variables
   - Lägg till: ANTHROPIC_API_KEY = din-nyckel
   - (Hämta din nyckel på https://console.anthropic.com)
4. Railway ger dig en URL automatiskt — dela den med vem du vill!

## Deploya på Render (alternativ)

1. Skapa konto på https://render.com
2. New → Web Service → koppla ditt GitHub-repo
3. Build Command: pip install -r requirements.txt
4. Start Command: gunicorn app:app
5. Lägg till ANTHROPIC_API_KEY under Environment

## Köra lokalt

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=din-nyckel
python app.py
```
Öppna http://localhost:5000
