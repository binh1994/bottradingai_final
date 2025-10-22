import os
from openai import OpenAI
import requests
import random
import datetime

# ===============================
# 🔑 CẤU HÌNH API KEY
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ===============================
# 🧠 TẠO NỘI DUNG BÀI VIẾT
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
    print(f"\n🧠 Requesting article from OpenAI for topic: {topic}")
    prompt = f"Write an SEO-friendly blog post titled '{topic}' for US, UK, and EU readers. Include intro, subheadings, and conclusion in HTML-ready format."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert financial and AI blog writer."},
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
        title = topic
        print(f"✅ Article generated (approx length chars): {len(content)}")
        return title, content
    except Exception as e:
        print(f"❌ Error generating article: {e}")
        return None, None


# ===============================
# 🖼️ TẠO HOẶC TÌM ẢNH MINH HỌA
# ===============================
def generate_image(topic):
    print(f"\n🖼️ Requesting image from OpenAI (1024x1024)...")
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=f"A professional AI trading themed photo about {topic}, 16:9 ratio, ultra-realistic, suitable for tech news website.",
            size="1024x1024"
        )
        image_url = result.data[0].url
        print("✅ OpenAI image generated successfully.")
        return image_url
    except Exception as e:
        print(f"⚠️ Image generation failed: {e}")
        print("🔁 Trying Pixabay fallback...")
        return get_pixabay_image(topic)


# ===============================
# 🖼️ TẢI ẢNH TỪ PIXABAY
# ===============================
def get_pixabay_image(query):
    if not PIXABAY_API_KEY:
        print("❌ Pixabay API key not found.")
        return None
    try:
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=50"
        response = requests.get(url)
        data = response.json()
        if "hits" in data and len(data["hits"]) > 0:
            hit = random.choice(data["hits"])
            print(f"✅ Pixabay image found: {hit['webformatURL']}")
            return hit["webformatURL"]
        else:
            print("❌ No Pixabay images found for query.")
            return None
    except Exception as e:
        print(f"❌ Error fetching Pixabay image: {e}")
        return None


# ===============================
# 💾 LƯU FILE HTML RA THƯ MỤC OUTPUT
# ===============================
def save_post(title, content, image_url):
    os.makedirs("output", exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"output/{date_str}_{title.replace(' ', '_')}.html"

    GA_CODE = """
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-33MQNED7W8"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-33MQNED7W8');
    </script>
    """

    AD_SCRIPT = """
    <!-- Ad Script -->
    <script async="async" data-cfasync="false" src="//pl27891709.effectivegatecpm.com/4955a0184593e15cf0c89752f04aab3a/invoke.js"></script>
    <div id="container-4955a0184593e15cf0c89752f04aab3a"></div>
    """

    html = f"""
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | BotTradingAI</title>
        <meta name="description" content="{title[:150]}">
        {GA_CODE}
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 780px; margin: auto; line-height: 1.7; background: #fdfdfd; color: #222; }}
            img {{ width: 100%; border-radius: 8px; margin-bottom: 20px; }}
            header, footer {{ text-align: center; margin: 30px 0; }}
            h1 {{ color: #0b3954; }}
            a {{ color: #0073e6; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <header>
            <h1><a href="https://bottradingai.com">BotTradingAI</a></h1>
            <p>Your AI-Powered Trading News Source</p>
        </header>

        <main>
            <h2>{title}</h2>
            <p><i>Published on {datetime.date.today().strftime("%B %d, %Y")}</i></p>
            {'<img src="' + image_url + '">' if image_url else ''}
            <div>{content}</div>
        </main>

        <footer>
            <p>© 2025 BotTradingAI | <a href="https://afternic.com/domain/bottradingai.com">Buy This Domain</a></p>
            {AD_SCRIPT}
        </footer>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Post HTML created: {filename}")


# ===============================
# 🚀 CHẠY TOÀN BỘ QUY TRÌNH
# ===============================
def main():
    title, content = generate_post()
    if not content:
        return
    image_url = generate_image(title)
    save_post(title, content, image_url)
    print("\n🎉 All done – Article & image generated successfully!")


if __name__ == "__main__":
    main()
