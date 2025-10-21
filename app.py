# app.py - News-style AI Magazine with local 24h background generator & manual 'Generate Now'
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import os, threading, time
from datetime import datetime
from auto_generate import main as generate_once

app = Flask(__name__, static_folder='static', template_folder='templates')

POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")
os.makedirs(POSTS_DIR, exist_ok=True)

def list_posts():
    posts = []
    for f in sorted(os.listdir(POSTS_DIR), reverse=True):
        if f.endswith(".html"):
            path = os.path.join(POSTS_DIR, f)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
            except:
                mtime = ""
            posts.append({"filename": f, "date": mtime, "title": extract_title(path), "excerpt": extract_excerpt(path)})
    return posts

def extract_title(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            txt = f.read(2000)
            import re
            m = re.search(r"<h2>(.*?)</h2>", txt, re.IGNORECASE|re.DOTALL)
            if m:
                return m.group(1).strip()
    except:
        pass
    return filepath

def extract_excerpt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            txt = f.read(4000)
            import re
            m = re.search(r"<p>(.*?)</p>", txt, re.IGNORECASE|re.DOTALL)
            if m:
                return (m.group(1).strip()[:220] + "...") if len(m.group(1).strip())>220 else m.group(1).strip()
    except:
        pass
    return ""

@app.route("/")
def index():
    posts = list_posts()
    return render_template("index.html", posts=posts, year=datetime.now().year)

@app.route("/posts/<path:filename>")
def posts(filename):
    full = os.path.join(POSTS_DIR, filename)
    if os.path.exists(full):
        with open(full, "r", encoding="utf-8") as f:
            html = f.read()
        return html
    abort(404)

@app.route("/about")
def about():
    return render_template("about.html", year=datetime.now().year)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name","")
        email = request.form.get("email","")
        message = request.form.get("message","")
        now = datetime.now().isoformat()
        log = f"{now}\t{name}\t{email}\t{message}\n"
        with open(os.path.join(os.path.dirname(__file__), "messages.txt"), "a", encoding="utf-8") as f:
            f.write(log)
        return redirect(url_for('contact') + "?sent=1")
    sent = request.args.get("sent","")
    return render_template("contact.html", sent=sent, year=datetime.now().year)

@app.route("/generate-now", methods=["POST"])
def generate_now():
    # spawn a background thread to generate to avoid blocking the web request
    thread = threading.Thread(target=generate_once)
    thread.start()
    return jsonify({"status":"started"}), 202

def background_scheduler():
    # Run generate_once() immediately on start, then every 24h.
    try:
        while True:
            try:
                print("Background generator running: generating post...")
                generate_once()
            except Exception as e:
                print("Background generator error:", e)
            # sleep 24 hours
            time.sleep(24*3600)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    # start background scheduler thread
    t = threading.Thread(target=background_scheduler, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
