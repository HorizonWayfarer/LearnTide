"""Parse front-matter markdown for publish queue."""
import json
import re
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def parse_front_matter(filepath: str) -> Dict[str, Any]:
    """Parse a markdown file with YAML-style front-matter."""
    path = Path(filepath) if not str(filepath).startswith("/") else Path(filepath)
    if not path.is_absolute():
        path = BASE_DIR / path
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*?)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"No front-matter found in {filepath}")
    fm_text, body = match.group(1), match.group(2)
    fm: Dict[str, Any] = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            # Strip quotes
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                v = v[1:-1]
            fm[k] = v
    fm["_file"] = str(path)
    fm["_body"] = body
    return fm

def get_pending(queue_dir: str, platform: str = None):
    """Return list of pending publish files."""
    config = json.loads((Path(__file__).resolve().parent / "config.json").read_text(encoding="utf-8"))
    qdir = BASE_DIR / config["publish_queue_dir"]
    results = []
    for f in sorted(qdir.glob("*.md")):
        try:
            fm = parse_front_matter(str(f))
            if fm.get("status", "pending") == "pending":
                if platform is None or fm.get("platform") == platform:
                    results.append(fm)
        except:
            pass
    return results
