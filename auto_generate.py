# auto_generate.py - generate one SEO article and save as HTML into posts/
import os, datetime, re
try:
    import openai
except Exception as e:
    print("Missing openai client. Install with: pip install openai==0.28")
    raise

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("OPENAI_API_KEY environment variable is not set. Set it on Render or locally.")
    raise SystemExit(1)
openai.api_key = OPENAI_KEY

MODEL = "gpt-3.5-turbo"
POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")
os.makedirs(POSTS_DIR, exist_ok=True)

def slugify(text):
    s = text.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s[:80]

def build_prompt(topic, keywords):
    prompt = f"""You are a professional SEO content writer for an AI trading magazine.     Write a long-form SEO-optimized article in English about: {topic}.     Include an SEO-friendly title (<=70 chars), a meta description (<=160 chars), and the article content     of roughly 800-1100 words. Use subheadings, short paragraphs, and include the following keywords organically: {', '.join(keywords)}.     Return a JSON object only with keys: title, meta, content (where content is HTML-ready)."""
    return prompt

def generate(topic, keywords):
    prompt = build_prompt(topic, keywords)
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"system","content":"You are a helpful SEO writer."},
                  {"role":"user","content":prompt}],
        max_tokens=1400,
        temperature=0.65
    )
    text = resp['choices'][0]['message']['content'].strip()
    # attempt to find JSON in response
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        j = text[start:end+1]
        try:
            import json
            obj = json.loads(j)
            return obj.get('title','Untitled'), obj.get('meta',''), obj.get('content','')
        except:
            pass
    # fallback
    return f"AI Market Insights - {datetime.date.today().isoformat()}", "AI Market Insights", text

def save_post(title, meta, content):
    date_str = datetime.date.today().isoformat()
    slug = slugify(title)
    filename = f"{date_str}-{slug}.html"
    filepath = os.path.join(POSTS_DIR, filename)
    tpl_path = os.path.join(os.path.dirname(__file__), 'templates', 'post.html')
    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    html = tpl.replace('{{POST_TITLE}}', title).replace('{{POST_META}}', meta).replace('{{POST_CONTENT}}', content).replace('{{POST_DATE}}', date_str)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath

def main():
    topic = "AI in trading: automated strategies, market signals, and AI tools for traders"
    keywords = ["AI trading", "automated trading", "market insights", "algo trading", "trading signals"] 
    print('Generating article...')
    title, meta, content = generate(topic, keywords)
    path = save_post(title, meta, content)
    print('Saved:', path)

if __name__ == '__main__':
    main()
