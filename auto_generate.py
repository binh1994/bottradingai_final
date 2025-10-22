import os
from openai import OpenAI
import requests
import random
import datetime

# ===============================
# 🔑 API KEYS
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ===============================
# 🧠 TẠO NỘI DUNG
# ===============================
def generate_post():
    topics = [
        "AI-driven stock trading strategies for 2025",
        "The rise of autonomous trading bots in global markets",
        "How machine learning is transforming crypto investments",
        "Predictive analytics and the future of forex trading",
        "AI regulation and ethics in algorithmic trading",
        "Top 5 AI tools changing the investment landscape",
        "How GPT-powered bots make smarter trading decisions"
    ]
    topic = random.choice(topics)
    print(f"\n🧠 Generating article: {topic}")

    prompt = f"Write an SEO-friendly blog post titled '{topic}' in English for trading audiences. Include intro, sections, and conclusion in HTML format."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert AI trading blogger."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
        return topic, content
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        return None, None

# ===============================
# 🖼 TẠO ẢNH
# ===============================
def generate_image(topic):
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=f"A professional AI trading themed image about {topic}, realistic, 16:9 ratio",
            size="1024x1024"
        )
        image_url = result.data[0].url
        print("✅ Image generated successfully.")
        return image_url
    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        return None

# ===============================
# 💾 LƯU FILE MARKDOWN (_posts)
# ===============================
def save_post(title, content, image_url):
    os.makedirs("_posts", exist_ok=True)
    date = datetime.date.today().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "_").replace("/", "_")
    filename = f"_posts/{date}-{slug}.md"

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
description: "{title[:150]}"
image: "{image_url if image_url else ''}"
---\n
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(f"{GA_CODE}\n\n")
        f.write(f"<h2>{title}</h2>\n")
        f.write(f"<p><i>Published on {datetime.date.today().strftime('%B %d, %Y')}</i></p>\n")
        if image_url:
            f.write(f'<img src="{image_url}" alt="{title}">\n\n')
        f.write(content)
        f.write(f"\n\n{AD_SCRIPT}")

    print(f"✅ Post saved as: {filename}")
    return filename

# ===============================
# 🚀 MAIN
# ===============================
def main():
    title, content = generate_post()
    if not content:
        print("❌ No content generated.")
        return
    image_url = generate_image(title)
    save_post(title, content, image_url)
    print("\n🎉 Done — post generated successfully!")

if __name__ == "__main__":
    main()
