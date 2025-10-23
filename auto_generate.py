import os, random, datetime
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# 1️⃣ Sinh bài viết AI có mở đầu + backlink + related articles
# ==========================================
def generate_post():
    topics = [
        "AI-driven stock trading strategies for 2025",
        "How AI is transforming crypto investments",
        "Predictive analytics and forex trading",
        "AI in portfolio optimization",
        "Top 5 AI trading bots outperforming humans",
    ]
    topic = random.choice(topics)
    prompt = f"""
Write a Markdown SEO blog post titled '{topic}' (English).
Add a human intro:
"In today’s fast-moving AI-driven markets, traders are adapting faster than ever. Let’s break down what’s happening in 2025..."
Include 3 sections + conclusion.
Author: 'By Alex Reed – AI Financial Analyst'.
At the end, add "### Related Articles" with 3 fake internal links using Markdown.
Naturally insert backlinks (one of these domains) inside content:
botblockchain.io, botgame.io, metaversebot.io, nftgameai.com, hubgaming.io, botdefi.io, esportsai.io,
nftgamepro.com, botesports.com, aiesports.io, pronftgame.com, botplay.io, botweb3ai.com, bottradingai.com
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert AI financial blogger who writes engaging SEO content."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
        return topic, content
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        return None, None


# ==========================================
# 2️⃣ Gắn ảnh Unsplash ngẫu nhiên
# ==========================================
def get_random_unsplash():
    tags = ["ai", "finance", "trading", "technology", "investment"]
    tag = random.choice(tags)
    return f"https://source.unsplash.com/800x450/?{tag},{random.choice(tags)}"


# ==========================================
# 3️⃣ Lưu file Markdown hợp lệ cho Jekyll
# ==========================================
def save_post(title, content):
    os.makedirs("_posts", exist_ok=True)
    date = datetime.date.today().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("/", "-")
    filename = f"_posts/{date}-{slug}.md"

    image_url = get_random_unsplash()

    ad_code = """<!-- Ad -->
<div class="ad-banner" style="text-align:center;margin:20px auto;">
  <script async="async" data-cfasync="false"
    src="//pl27891709.effectivegatecpm.com/4955a0184593e15cf0c89752f04aab3a/invoke.js">
  </script>
  <div id="container-4955a0184593e15cf0c89752f04aab3a"></div>
  <iframe src="//pl27891709.effectivegatecpm.com/4955a0184593e15cf0c89752f04aab3a/invoke.js" 
    style="width:300px;height:250px;border:none;overflow:hidden;"></iframe>
</div>"""

    front = f"""---
layout: post
title: "{title}"
date: {datetime.datetime.now().isoformat()}
description: "{title} - AI trading insights"
image: "{image_url}"
---
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front)
        f.write(ad_code + "\n")
        f.write(content)
        f.write("\n\n" + ad_code)

    print(f"✅ Generated: {filename}")


# ==========================================
# 4️⃣ MAIN
# ==========================================
def main():
    title, content = generate_post()
    if not content:
        return
    save_post(title, content)
    print("\n🎉 Post generated with Unsplash image + ad + backlinks!")


if __name__ == "__main__":
    main()
