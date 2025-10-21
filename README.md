BotTradingAI - Final Light (news magazine)
-----------------------------------------
This package is pre-configured as a light-theme AI news magazine.
- Homepage lists latest AI-generated posts.
- auto_generate.py creates one SEO article using OPENAI_API_KEY (set as env var).
- Background thread in app.py runs generate once at startup and every 24h thereafter.
- Do NOT include API keys in files. Use Render Environment variables or setx locally.

Local test:
  pip install -r requirements.txt
  setx OPENAI_API_KEY "sk-NEWKEY"  # then restart CMD
  python app.py
  # background generator runs at startup and every 24h. You can also click "Generate Now" on homepage.

Deploy on Render:
  - Push repo to GitHub
  - Create Web Service on Render, link the repo
  - Build: pip install -r requirements.txt
  - Start: gunicorn app:app
  - Add Environment: OPENAI_API_KEY (your key), FLASK_ENV=production
  - (Optional) Use Render Cron if you prefer scheduler.
