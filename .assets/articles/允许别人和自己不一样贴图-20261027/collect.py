"""保存公开网页或页面默认只读接口的调研快照，不携带登录凭据。"""
import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent


class PublicPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.scripts = []
        self.images = []
        self.metadata = {}
        self.skip = 0
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "meta":
            name = attrs.get("property") or attrs.get("name")
            if name in ("description", "og:title", "og:description", "og:image", "article:published_time"):
                self.metadata[name] = attrs.get("content", "")
        if tag == "img":
            src = attrs.get("data-src") or attrs.get("src", "")
            if src.startswith(("http://", "https://")):
                self.images.append({"url": src, "alt": attrs.get("alt", "")})
        if tag == "a":
            self.anchor = {"url": attrs.get("href", ""), "text": []}

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag == "a" and self.anchor is not None:
            self.anchor["text"] = " ".join(self.anchor["text"])
            self.links.append(self.anchor)
            self.anchor = None

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())
            if self.anchor is not None:
                self.anchor["text"].append(data.strip())


def collect(label, url, mode):
    record = {"url": url, "accessed_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat()}
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"})
        with urlopen(req, timeout=30) as response:
            record.update(status=response.status, final_url=response.url)
            body = response.read().decode("utf-8", errors="replace")
        if mode == "json":
            record["data"] = json.loads(body)
        else:
            page = PublicPage()
            page.feed(body)
            record.update(text="\n".join(page.text), links=page.links, scripts=page.scripts,
                          images=page.images, metadata=page.metadata)
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    folder = ROOT / "snapshots"
    folder.mkdir(exist_ok=True)
    (folder / f"{label}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("url")
    parser.add_argument("--mode", choices=["json", "html"], default="html")
    args = parser.parse_args()
    record = collect(args.label, args.url, args.mode)
    if "data" in record:
        payload = record["data"]
        result = payload.get("data", {}) if isinstance(payload, dict) else {}
        print(json.dumps({"label": args.label, "status": record.get("status"),
                          "code": payload.get("code"), "message": payload.get("message"),
                          "stat_date": result.get("stat_date"), "total": result.get("total"),
                          "records": len(result.get("list", []))}, ensure_ascii=False))
    else:
        print(json.dumps({"label": args.label, "status": record.get("status"),
                          "error": record.get("error"), "text": record.get("text", "")[:8000]},
                         ensure_ascii=False))
