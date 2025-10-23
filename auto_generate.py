import os
import random
import datetime
import requests
from openai import OpenAI

# ===============================
# 🔑 API SETUP
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ===============================
# 🌐 DANH SÁCH DOMAIN BACKLINK
# ===============================
BACKLINK_DOMAINS = [
    "botblockchain.io", "botgame.io", "metaversebot.io", "nftgameai.com",
    "hubgaming.io", "botdefi.io", "esportsai.io", "nftgamepro.com",
    "botesports.com", "aiesports.io", "pronftgame.com", "botplay.io",
    "botweb3ai.com", "bottradingai.com"
]

# ===============================
# 🧠 SINH BÀI VIẾT
# ===============================
def generate_post():
    topics = [
        "AI-driven stock trading strategies for 2025",
        "How GPT-powered bots are changing forex trading",
        "Predictive analytics in cryptocurrency markets",
        "Top 5 AI trading models outperforming humans",
        "How AI is redefining risk management in investing",
        "The rise of algorithmic bots in DeFi platforms",
        "Ethical AI in finance: where do we draw the line?"
    ]
    topic = random.choice(topics)
    print(f"\n🧠 Generating article: {topic}")

    intro = (
        "In today’s fast-moving AI-driven markets, traders are adapting faster than ever. "
        "Let’s break down what’s happening in 2025 and how innovation is reshaping finance."
    )

    prompt = f"""
Write a detailed **Markdown-formatted** SEO blog post titled '{topic}'.
Audience: investors, fintech professionals, and AI enthusiasts.
Include:
- Engaging introduction
- 3 clear sections with subtitles
- A conclusion
Add 1–2 markdown images (![alt text](IMAGE_PLACEHOLDER)).
Include relevant keywords naturally (AI trading, algorithmic investing, GPT bots).
Avoid HTML tags.
At the end, add a short related summary.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert AI finance writer."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
        return topic, intro, content
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        return None, None, None

# ===============================
# 💾 LƯU FILE MARKDOWN
# ===============================
def save_post(title, intro, content):
    os.makedirs("_posts", exist_ok=True)
    date = datetime.date.today().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("/", "-")
    filename = f"_posts/{date}-{slug}.md"

    # 🔗 Chọn 3 backlink ngẫu nhiên
    backlinks = random.sample(BACKLINK_DOMAINS, 3)
    backlinks_html = " | ".join(
        [f'<a href="https://{link}" target="_blank" rel="noopener noreferrer">{link}</a>' for link in backlinks]
    )

    # 🖼️ Ảnh từ Unsplash
    image_url = f"https://source.unsplash.com/800x400/?ai,trading,finance,{slug}"

    # 🧩 Quảng cáo & GA
    GA_CODE = """<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-33MQNED7W8"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-33MQNED7W8');
</script>"""

    AD_SCRIPT = """<!-- Ad Script -->
<script async="async" data-cfasync="false" src="//pl27891709.effectivegatecpm.com/4955a0184593e15cf0c89752f04aab3a/invoke.js"></script>
<div id="container-4955a0184593e15cf0c89752f04aab3a"></div>"""

    front_matter = f"""---
layout: post
title: "{title}"
date: {datetime.datetime.now().isoformat()}
author: "Alex Reed – AI Financial Analyst"
description: "{title} — Insights into the evolving world of AI trading and finance."
image: "{image_url}"
---"""

    related = """
<hr>
<h3>🧭 Related Articles</h3>
<ul>
{% for post in site.posts limit:3 %}
  {% if post.url != page.url %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
"""

    # ✍️ Ghi nội dung file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + "\n\n")
        f.write(GA_CODE + "\n\n")
        f.write(f"![AI Trading]({image_url})\n\n")
        f.write(f"_{intro}_\n\n")
        f.write(content.strip())
        f.write("\n\n---\n\n")
        f.write(f"<p><b>Explore more from our AI network:</b><br>{backlinks_html}</p>\n")
        f.write(related)
        f.write("\n\n" + AD_SCRIPT)

    print(f"✅ Post saved as: {filename}")
    return filename

# ===============================
# 🔍 Ping Google để index bài mới
# ===============================
def ping_google():
    sitemap_url = "https://bottradingai.com/sitemap.xml"
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    try:
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print("✅ Google pinged successfully.")
        else:
            print(f"⚠️ Google ping failed: {r.status_code}")
    except Exception as e:
        print(f"❌ Ping error: {e}")

# ===============================
# 🚀 MAIN
# ===============================
def main():
    title, intro, content = generate_post()
    if not content:
        print("❌ No content generated.")
        return
    save_post(title, intro, content)
    ping_google()
    print("\n🎉 Done — SEO article generated & Google notified!")

if __name__ == "__main__":
    main()
