import os
import re
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_PATH = Path(os.environ.get("MEMORY_PATH", "./memory"))


def read_context() -> str:
    parts = []

    for filename in ["core.md", "learning.md", "goals.md"]:
        path = MEMORY_PATH / "compiled" / filename
        if path.exists():
            parts.append(f"## {filename}\n{path.read_text(encoding='utf-8')}")

    wiki = MEMORY_PATH / "wiki" / "index.md"
    if wiki.exists():
        parts.append(f"## wiki/index.md\n{wiki.read_text(encoding='utf-8')}")

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


def update_streak():
    """Increment streak in learning.md if not already counted today. Resets to 1 if gap > 1 day."""
    path = MEMORY_PATH / "compiled" / "learning.md"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    streak_match = re.search(r"Текущий: (\d+) дней подряд", content)
    date_match = re.search(r"Последний день учёбы: (\d{4}-\d{2}-\d{2})", content)

    current_streak = int(streak_match.group(1)) if streak_match else 0
    last_date = date_match.group(1) if date_match else None

    if last_date == today:
        return  # Уже засчитан сегодня

    new_streak = current_streak + 1 if last_date == yesterday else 1

    if streak_match:
        content = content.replace(streak_match.group(0), f"Текущий: {new_streak} дней подряд")
    if date_match:
        content = content.replace(date_match.group(0), f"Последний день учёбы: {today}")

    path.write_text(content, encoding="utf-8")


def read_compiled(filename: str) -> str:
    path = MEMORY_PATH / "compiled" / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_compiled(filename: str, content: str):
    path = MEMORY_PATH / "compiled" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
