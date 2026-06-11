import os
import sqlite3
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

MEMORY_PATH = Path(os.environ.get("MEMORY_PATH", "./memory"))
KB_PATH = Path(os.environ.get("KB_PATH", "./knowledge-base/aizdec"))
DB_PATH = os.environ.get("DB_PATH", "./logs.db")

mcp = FastMCP("telegramassist-memory")


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@mcp.tool()
def read_memory(files: list[str]) -> dict[str, str]:
    """Read memory files. Pass relative paths like 'compiled/core.md'."""
    result = {}
    for f in files:
        path = MEMORY_PATH / f
        if path.exists():
            result[f] = path.read_text(encoding="utf-8")
        else:
            result[f] = f"[file not found: {f}]"
    return result


@mcp.tool()
def write_memory(file: str, content: str) -> str:
    """Write or overwrite a memory file. Pass relative path like 'compiled/core.md'."""
    path = MEMORY_PATH / file
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Written: {file}"


@mcp.tool()
def append_memory(file: str, content: str) -> str:
    """Append content to a memory file."""
    path = MEMORY_PATH / file
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n{content}\n")
    return f"Appended to: {file}"


@mcp.tool()
def search_memory(query: str) -> list[dict]:
    """Search all memory files for a query string. Returns list of matches."""
    matches = []
    for path in MEMORY_PATH.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if query.lower() in text.lower():
            rel = str(path.relative_to(MEMORY_PATH))
            lines = [l for l in text.splitlines() if query.lower() in l.lower()]
            matches.append({"file": rel, "matches": lines[:5]})
    return matches


@mcp.tool()
def search_knowledge_base(query: str, max_results: int = 3) -> list[dict]:
    """Search aizdec course lessons by keywords. Returns lesson title, course, and full content."""
    if not KB_PATH.exists():
        return [{"error": "Knowledge base not found"}]

    query_words = [w.lower() for w in query.split() if len(w) > 2]
    if not query_words:
        return []

    scored = []
    for path in KB_PATH.rglob("*.md"):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        text_lower = text.lower()
        score = sum(text_lower.count(w) for w in query_words)
        if score > 0:
            lines = text.splitlines()
            title = lines[0].lstrip("# ").strip() if lines else path.stem
            course = path.parent.name
            scored.append({"score": score, "title": title, "course": course, "content": text, "path": str(path)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return [
        {"title": r["title"], "course": r["course"], "content": r["content"]}
        for r in scored[:max_results]
    ]


@mcp.tool()
def list_knowledge_base() -> dict[str, list[str]]:
    """List all available course lessons grouped by course."""
    if not KB_PATH.exists():
        return {}
    result = {}
    for course_dir in sorted(KB_PATH.iterdir()):
        if course_dir.is_dir():
            lessons = []
            for f in sorted(course_dir.glob("*.md")):
                text = f.read_text(encoding="utf-8", errors="ignore")
                title = text.splitlines()[0].lstrip("# ").strip() if text else f.stem
                lessons.append(title)
            result[course_dir.name] = lessons
    return result


@mcp.tool()
def get_lesson(course: str, slug: str) -> str:
    """Get full content of a specific lesson. E.g. course='claude-code', slug='what-is-claude-code'."""
    path = KB_PATH / course / f"{slug}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"[Урок не найден: {course}/{slug}]"


@mcp.tool()
def log_conversation(message: str, response: str) -> str:
    """Save a conversation turn to SQLite."""
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO conversations (ts, message, response) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), message, response),
    )
    conn.commit()
    conn.close()
    return "Logged"


@mcp.tool()
def list_memory_files() -> list[str]:
    """List all files in the memory directory."""
    return [str(p.relative_to(MEMORY_PATH)) for p in MEMORY_PATH.rglob("*.md")]


if __name__ == "__main__":
    _init_db()
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
