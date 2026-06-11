import os
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_PATH = Path(os.environ.get("MEMORY_PATH", "./memory"))


def read_context() -> str:
    parts = []

    for filename in ["core.md", "learning.md", "goals.md"]:
        path = MEMORY_PATH / "compiled" / filename
        if path.exists():
            parts.append(f"## {filename}\n{path.read_text(encoding='utf-8')}")

    for i in range(3):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_path = MEMORY_PATH / "raw" / f"{date}.md"
        if log_path.exists():
            parts.append(f"## Log {date}\n{log_path.read_text(encoding='utf-8')}")

    return "\n\n".join(parts)


def append_to_log(text: str):
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = MEMORY_PATH / "raw" / f"{today}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%H:%M")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n### {timestamp}\n{text}\n")


def read_compiled(filename: str) -> str:
    path = MEMORY_PATH / "compiled" / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_compiled(filename: str, content: str):
    path = MEMORY_PATH / "compiled" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
