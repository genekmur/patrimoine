"""Local Python server and lightweight progress API for the OPSIE study site."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, sqlite3

ROOT = Path(__file__).resolve().parent
DB = ROOT / "work-progress.sqlite3"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            body = json.dumps({"ok": True, "course": "OPSIE"}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        if self.path.startswith("/api/progress/"):
            key = self.path.rsplit("/", 1)[-1]
            with sqlite3.connect(DB) as db:
                db.execute("CREATE TABLE IF NOT EXISTS progress (learner TEXT PRIMARY KEY, value TEXT NOT NULL)")
                row = db.execute("SELECT value FROM progress WHERE learner=?", (key,)).fetchone()
            body = (row[0] if row else "{}").encode()
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        return super().do_GET()

    def do_POST(self):
        if not self.path.startswith("/api/progress/"):
            self.send_error(404); return
        key = self.path.rsplit("/", 1)[-1]
        length = min(int(self.headers.get("Content-Length", "0")), 1_000_000)
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
            with sqlite3.connect(DB) as db:
                db.execute("CREATE TABLE IF NOT EXISTS progress (learner TEXT PRIMARY KEY, value TEXT NOT NULL)")
                db.execute("INSERT INTO progress VALUES (?, ?) ON CONFLICT(learner) DO UPDATE SET value=excluded.value", (key, json.dumps(value, ensure_ascii=False)))
            self.send_response(204); self.end_headers()
        except (ValueError, UnicodeDecodeError):
            self.send_error(400, "Invalid JSON")

if __name__ == "__main__":
    print("OPSIE study site: http://127.0.0.1:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
