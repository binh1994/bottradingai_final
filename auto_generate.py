import openai, os, random, datetime, requests, base64
from pathlib import Path

# === CONFIG ===
OUTPUT = Path("output")
POSTS = OUTPUT / "posts"
POSTS.mkdir(parents=True, exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

SITE_NAME = "BotTradingAI - Global AI Trading News"
DOMAIN = "https://bottradingai.com"
GOOGLE_ANALYTICS = "G-33MQNED7W8"
AD_SCRIPT = """
<script async="async" data-cfasync="false" src="//pl27891709.effectivegatecpm.com/4955a0184593e15cf0c89752f04aab3a/invoke.js"></script>
<div id="container-4955a0184593e15cf0c89752f04aab3a"></div>
"""

topics = [
    "AI-driven stock trading strategies for 2025",
    "The rise of autonomous trading bots in global markets",
    "How machine learning is transforming crypto investments",
    "Predictive analytics and the future of forex trading",
    "AI regulation and ethics in algorithmic trading",
    "Top 5 AI tools changing the investment landscape",
    "How GPT-powered bots make smarter trading decisions",
]

def generate_post():
    topic = random.choice(topics)
    prompt = f"""
Write a 700-word SEO-optimized article in English for readers in the US, UK, and Canada.
Topic: "{topic}".
Use professional tone (like Forbes, Cointelegraph, or TechCrunch).
Include a clear title, introduction, subheadings, and conclusion.
Output only the article content (HTML-friendly).
"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return topic, response.choices[0].message.content

# === Generate AI thumbnail using DALL·E ===
def generate_image(title):
    try:
        prompt = f"A professional AI trading themed photo for an article titled '{title}', futuristic, 16:9 ratio, ultra-realistic, suitable for tech news website."
        result = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1200x630"
        )
        image_data = base64.b64decode(result.data[0].b64_json)
        filename = f"{datetime.date.today()}_{title[:40].replace(' ','_')}.jpg"
        with open(POSTS / filename, "wb") as f:
            f.write(image_data)
        return filename
    except Exception as e:
        print("⚠️ Image generation failed:", e)
        return None

# === Create full article HTML ===
def create_post_html(title, content, image_filename):
    date = datetime.date.today().strftime("%B %d, %Y")
    desc = title[:150]
    img_tag = f"<img src='{image_filename}' alt='{title}'>" if image_filename else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {SITE_NAME}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{DOMAIN}/posts/{image_filename}">
<link rel="stylesheet" href="../styles.css">
{AD_SCRIPT}
</head>
<body>
<header>
  <h1><a href="../index.html">{SITE_NAME}</a></h1>
  <nav>
    <a href="../index.html">Home</a>
    <a href="../about.html">About</a>
    <a href="../contact.html">Contact</a>
  </nav>
</header>
<main class="article">
  <h2>{title}</h2>
  <p class="date">📅 {date}</p>
  {img_tag}
  <div class="content">{content.replace('\n','<br>')}</div>
</main>
<footer>
  <p>© 2025 <a href="{DOMAIN}">{DOMAIN}</a> | <a href="https://afternic.com/domain/bottradingai.com">Buy Domain</a></p>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_ANALYTICS}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GOOGLE_ANALYTICS}');</script>
</footer>
</body>
</html>"""
    filename = f"{datetime.date.today()}_{title[:40].replace(' ','_')}.html"
    (POSTS / filename).write_text(html, encoding="utf-8")
    return filename

# === Update homepage ===
def update_homepage():
    posts = sorted(POSTS.glob("*.html"), reverse=True)
    cards = ""
    for p in posts:
        img = str(p.with_suffix(".jpg").name)
        cards += f"""
        <div class='card'>
          <a href='posts/{p.name}'>
            <img src='posts/{img}' alt='{p.stem}'>
            <h3>{p.stem.replace('_',' ')}</h3>
          </a>
        </div>"""
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_NAME}</title>
<meta name="description" content="Latest AI trading, crypto, and investment automation news.">
<link rel="stylesheet" href="styles.css">
</head><body>
<header>
  <h1>{SITE_NAME}</h1>
  <nav>
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
    <a href="contact.html">Contact</a>
  </nav>
</header>
<main>
  <h2>Latest AI & Trading Insights</h2>
  <div class="grid">{cards}</div>
</main>
<footer>{AD_SCRIPT}</footer>
</body></html>"""
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")

# === MAIN ===
title, content = generate_post()
img = generate_image(title)
create_post_html(title, content, img)
update_homepage()
print("✅ Article & image generated successfully.")
