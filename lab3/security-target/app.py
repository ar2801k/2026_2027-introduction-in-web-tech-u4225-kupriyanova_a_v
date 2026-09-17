from flask import Flask, request, Response
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path("/app/files")


@app.route("/")
def index():
    return """
    <h1>Lab3 Security Target</h1>
    <p>Local training application for security testing.</p>
    <ul>
        <li><a href="/health">Health</a></li>
        <li><a href="/download?file=public.txt">Download public file</a></li>
    </ul>
    """


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/admin")
def admin():
    return "Training admin page"


@app.route("/backup")
def backup():
    return "Training backup directory"


@app.route("/config")
def config():
    return "Training configuration page"


@app.route("/download")
def download():
    filename = request.args.get("file", "public.txt")

    # Намеренно небезопасная реализация для учебной лабораторной работы:
    target = BASE_DIR / filename

    try:
        content = target.read_text(errors="ignore")
        return Response(content, mimetype="text/plain")
    except Exception:
        return Response("File not found", status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)