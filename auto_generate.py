import os
from openai import OpenAI
import random
import datetime

# ===============================
# 🔑 API KEYS
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

    prompt = f"""
Write a **Markdown-formatted** SEO blog post titled '{topic}'.
- Audience: AI trading & investing.
- Include: introduction, 3 sections, and a conclusion.
- Add 1-2 markdown images (use ![alt text](IMAGE_PLACEHOLDER)).
- Add relevant keywords naturally.
- Do NOT include <!DOCTYPE html> or <html> tags.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert AI finance content writer."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
        return topic, content
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        return None, None

# ===============================
# 💾 LƯU FILE MARKDOWN (_posts)
# ===============================
def save_post(title, content, image_url):
    os.makedirs("_posts", exist_ok=True)
    date = datetime.date.today().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("/", "-")
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
description: "{title} — Learn how AI and automation are transforming finance."
image: "{image_url if image_url else '/assets/images/default-banner.jpg'}"
---
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(f"{GA_CODE}\n\n")
        f.write(content.strip())
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

    # Không cần tạo ảnh bằng AI để giảm dung lượng & tránh lỗi
    image_url = f"/assets/images/{title.lower().replace(' ', '_')}.jpg"
    save_post(title, content, image_url)
    print("\n🎉 Done — SEO post generated successfully!")

if __name__ == "__main__":
    main()
