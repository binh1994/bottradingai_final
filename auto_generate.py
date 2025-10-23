import os
import random
import datetime

# Danh sách domain trong hệ thống backlink
BACKLINK_DOMAINS = [
    "botblockchain.io", "botgame.io", "metaversebot.io", "nftgameai.com",
    "hubgaming.io", "botdefi.io", "esportsai.io", "nftgamepro.com",
    "botesports.com", "aiesports.io", "pronftgame.com",
    "botplay.io", "botweb3ai.com", "bottradingai.com"
]

# Từ khóa ảnh Unsplash (không dùng API, load nhanh)
IMAGE_KEYWORDS = ["ai", "trading", "finance", "blockchain", "crypto"]

def get_unsplash_image():
    keyword = random.choice(IMAGE_KEYWORDS)
    # Random ảnh miễn phí, dung lượng nhỏ
    return f"https://source.unsplash.com/random/800x500/?{keyword}"

def generate_backlinks():
    links = []
    for domain in random.sample(BACKLINK_DOMAINS, 4):
        links.append(f'<a href="https://{domain}" target="_blank" rel="nofollow">{domain}</a>')
    return " | ".join(links)

def generate_post(title, content):
    today = datetime.date.today().strftime("%B %d, %Y")
    image_url = get_unsplash_image()
    backlinks = generate_backlinks()

    # Giới thiệu tự nhiên
    intro = (
        "In today’s fast-moving AI-driven markets, traders are adapting faster than ever. "
        "Let’s break down what’s happening in 2025…"
    )

    author = "By Alex Reed – AI Financial Analyst"

    html = f"""---
layout: post
title: "{title}"
date: {today}
image: "{image_url}"
author: "{author}"
---

<img src="{image_url}" alt="{title}" loading="lazy" style="border-radius:12px; margin-bottom:20px;"/>

<p><strong>{author}</strong></p>
<p>{intro}</p>

{content}

<h3>Related Articles</h3>
<ul>
  <li><a href="/posts/">Explore more AI-driven trading insights</a></li>
  <li><a href="/">Visit our homepage for latest updates</a></li>
</ul>

<hr>
<p><strong>Partner Network:</strong> {backlinks}</p>
"""
    return html

if __name__ == "__main__":
    title = "How Machine Learning Is Changing Crypto Investments"
    body = """Machine learning is reshaping how investors approach crypto markets by using predictive analytics and automated strategies..."""
    post = generate_post(title, body)

    filename = f"_posts/{datetime.date.today()}-ai-post.html"
    os.makedirs("_posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(post)

    print("✅ New post generated:", filename)
