import os, openai, datetime, json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# --- Config ---
SITE_URL = "https://bottradingai.com"
POSTS_DIR = Path("posts")
TEMPLATES_DIR = Path("templates")
STATIC_IMG_DIR = Path("static/images")
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Ensure folders exist ---
POSTS_DIR.mkdir(exist_ok=True)
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

# --- Prompt setup ---
def generate_blog_post():
    topic_prompt = (
        "Generate a unique SEO-friendly blog post title and outline "
        "about trading bots, AI trading, or crypto investing. "
        "Use an educational yet friendly tone for American readers."
    )
    topic = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": topic_prompt}],
    ).choices[0].message.content.strip()

    content_prompt = (
        f"Write a 700-word article titled '{topic}' in English. "
        "Tone: Friendly and educational. "
        "Add clear structure, short paragraphs, SEO headings (h2/h3), and conclusion."
    )

    content = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content_prompt}],
    ).choices[0].message.content.strip()
    return topic, content


def generate_image(title):
    filename = STATIC_IMG_DIR / f"{title[:40].replace(' ', '_')}.png"
    try:
        img = openai.images.generate(model="gpt-image-1", prompt=f"Illustration about {title} in dark trading style")
        img_url = img.data[0].url
        os.system(f"curl -s {img_url} -o {filename}")
        return f"images/{filename.name}"
    except Exception as e:
        print("Image generation failed:", e)
        return "images/default.png"


def save_post(title, content, img_path):
    date_str = datetime.date.today().isoformat()
    slug = title.lower().replace(" ", "-").replace("/", "-")
    filename = POSTS_DIR / f"{slug}.html"

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("post.html")

    html = template.render(title=title, content=content, image=img_path, date=date_str, site_url=SITE_URL)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Created post: {filename}")


def main():
    title, content = generate_blog_post()
    img_path = generate_image(title)
    save_post(title, content, img_path)


if __name__ == "__main__":
    main()
