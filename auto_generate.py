import os
import random
import datetime
import re
import time
from openai import OpenAI

# ===========================
# 🔑 CONFIG
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
AUTHOR_NAME = "Alex Reed – AI Financial Analyst"

BACKLINK_DOMAINS = [
    "botblockchain.io", "botgame.io", "metaversebot.io", "nftgameai.com",
    "hubgaming.io", "botdefi.io", "esportsai.io", "nftgamepro.com",
    "botesports.com", "aiesports.io", "pronftgame.com",
    "botplay.io", "botweb3ai.com", "bottradingai.com"
]

TOPICS = [
    "Top 5 AI Trading Models Outperforming Humans",
    "AI-driven stock trading strategies for 2025",
    "How GPT-powered bots are changing forex trading",
    "Predictive analytics in cryptocurrency markets",
    "The rise of autonomous trading bots in global markets",
    "How AI is redefining risk management in investing",
    "Ethical AI in finance: what traders should know"
]

UNSPLASH_QUERIES = ["ai", "trading", "finance", "crypto", "stock", "data"]

# ===========================
# 🧠 GENERATE CONTENT
# ===========================
def generate_post():
    topic = random.choice(TOPICS)
    print(f"\n🧠 Generating SEO article: {topic}")

    prompt = f"""
Write a detailed, SEO-optimized blog post titled "{topic}" in Markdown format.
Include:
- A human-like intro paragraph (like a real writer).
- 3 main sections (use ## headings).
- A conclusion.
- Mention AI trading naturally.
- No HTML, only Markdown.
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional AI finance blogger."},
                {"role": "user", "content": prompt}
            ],
        )
        return topic, completion.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI Error:", e)
        return topic, "Content generation failed."

# ===========================
# 🖼 GET UNSPLASH IMAGE
# ===========================
def get_image():
    query = ",".join(random.sample(UNSPLASH_QUERIES, 2))
    return f"https://source.unsplash.com/800x400/?{query}"

# ===========================
# 🔗 ROTATE BACKLINKS
# ===========================
def get_backlinks():
    selected = random.sample(BACKLINK_DOMAINS, random.randint(2, 3))
    return [f"[{d}](https://{d})" for d in selected]

# ===========================
# 💾 SAVE POST
# ===========================
def save_post(title, content, image_url, backlinks):
    os.makedirs("_posts", exist_ok=True)
    date = datetime.date.today().strftime("%Y-%m-%d")
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    filename = f"_posts/{date}-{slug}.md"

    front_matter = f"""---
layout: post
title: "{title}"
date: {datetime.datetime.now().isoformat()}
description: "{title} — AI and trading insights for modern investors."
image: "{image_url}"
author: "{AUTHOR_NAME}"
---
"""

    # đoạn mở đầu “con người” + banner quảng cáo
    ad_block = "{% include ad.html %}\n\n"
    intro = "_In today’s fast-moving AI-driven markets, traders are adapting faster than ever. Let’s break down what’s happening in 2025 and how innovation is reshaping finance._\n\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(f"![{title}]({image_url})\n\n")
        f.write(f"*By {AUTHOR_NAME}*\n\n")
        f.write(intro)
        f.write(ad_block)
        f.write(content.strip())
        f.write("\n\n---\n\n### Related Articles\n")
        f.write("{% for p in site.posts limit:3 %}\n")
        f.write("  {% if p.url != page.url %}\n")
        f.write("  - [{{ p.title }}]({{ p.url }})\n")
        f.write("  {% endif %}\n")
        f.write("{% endfor %}\n\n")
        f.write(ad_block)
        f.write("**Explore more from our AI network:**  \n")
        f.write(" | ".join(backlinks))
        f.write("\n\n")
        f.write(ad_block)

    print(f"✅ Post saved as: {filename}")
    return filename

# ===========================
# 🚀 MAIN
# ===========================
def main():
    title, content = generate_post()
    image_url = get_image()
    backlinks = get_backlinks()
    save_post(title, content, image_url, backlinks)
    print("🎯 Done — post generated successfully with image, ads, backlinks, and SEO intro!")

if __name__ == "__main__":
    main()
