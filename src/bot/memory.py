import os
import re
from pathlib import Path
from datetime import datetime, timedelta

_DEFAULT_MEMORY = Path(__file__).resolve().parent.parent.parent / "memory"
MEMORY_PATH = Path(os.environ.get("MEMORY_PATH", str(_DEFAULT_MEMORY)))


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


_MODULE_NAMES = {
    1: "Старт и первый код",
    2: "Как правильно говорить с агентом",
    3: "Документ, который спасает проект от хаоса",
    4: "Сохраняем работу и выкладываем в интернет",
    5: "Даём агенту суперсилы",
    6: "Автономная работа агента",
    7: "Выкладываем продукт в интернет",
    8: "База данных",
    9: "Подключение оплат",
}


def parse_module_progress(text: str) -> tuple[int, int] | None:
    """Извлекает (модуль, урок) из текста типа '9 модуль 2 урок'. Возвращает None если не найдено."""
    low = text.lower()
    m = re.search(r'(\d+)\s*(?:модул[ьея]|module)', low)
    if not m:
        return None
    mod = int(m.group(1))
    if mod not in _MODULE_NAMES:
        return None
    l = re.search(r'(\d+)\s*(?:урок|lesson)', low)
    lesson = int(l.group(1)) if l else 1
    return mod, lesson


def update_learning_status(module: int, lesson: int) -> bool:
    """Обновляет статус модуля в learning.md: переключает эмодзи и ## Текущий статус."""
    path = MEMORY_PATH / "compiled" / "learning.md"
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    name = _MODULE_NAMES.get(module, f"Модуль {module}")

    # Обновляем текстовую строку статуса
    new_status = f"## Текущий статус\nНачат Модуль {module} — «{name}», Урок {lesson}"
    new_content = re.sub(r'## Текущий статус\n.*', new_status, content)

    # Снимаем 🔶 с прежнего активного модуля (кроме текущего)
    new_content = re.sub(
        rf'^(### )🔶( Модуль (?!{module}:)\d+:.+?)(?:\s*\(В ПРОЦЕССЕ\))?$',
        r'\1✅\2',
        new_content,
        flags=re.MULTILINE,
    )

    # Ставим 🔶 на текущий модуль (если он ещё ⬜)
    new_content = re.sub(
        rf'^(### )⬜( Модуль {module}:.+)$',
        r'\1🔶\2 (В ПРОЦЕССЕ)',
        new_content,
        flags=re.MULTILINE,
    )

    if new_content == content:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


_LEARNING_KEYWORDS = (
    "урок", "учился", "учился", "изучил", "прошел", "прошёл", "завершил",
    "посмотрел", "курс", "модул", "научился", "разобрался", "вайбкодинг",
    "claude code", "задание", "практик", "coding", "программирован",
)

_WORK_KEYWORDS = (
    "задачу", "задачи", "сделал", "выполнил", "закончил", "завершил",
    "работал", "работаю", "проект", "клиент", "встреча", "дедлайн",
    "созвон", "написал", "отправил", "запустил", "задеплоил",
)


def detect_learning(text: str) -> bool:
    """Возвращает True если в тексте упоминается учёба."""
    low = text.lower()
    return any(k in low for k in _LEARNING_KEYWORDS)


def detect_work(text: str) -> bool:
    """Возвращает True если в тексте упоминается работа."""
    low = text.lower()
    return any(k in low for k in _WORK_KEYWORDS)


_DAY_ALIASES = {
    "пн": "Пн", "понедельник": "Пн", "понедельника": "Пн",
    "вт": "Вт", "вторник": "Вт", "вторника": "Вт",
    "ср": "Ср", "среда": "Ср", "среду": "Ср", "среды": "Ср",
    "чт": "Чт", "четверг": "Чт", "четверга": "Чт",
    "пт": "Пт", "пятница": "Пт", "пятницу": "Пт", "пятницы": "Пт",
    "сб": "Сб", "суббота": "Сб", "субботу": "Сб", "субботы": "Сб",
    "вс": "Вс", "воскресенье": "Вс", "воскресенья": "Вс",
}


def detect_workout_day(text: str) -> str | None:
    """Возвращает аббревиатуру дня если в тексте есть упоминание тренировки+дня, иначе None."""
    low = text.lower()
    workout_keywords = ("тренировк", "пробежк", "бег", "сделал", "выполнил", "закончил", "готово", "✅", "забег")
    has_workout = any(k in low for k in workout_keywords)
    if not has_workout:
        return None
    for alias, abbr in _DAY_ALIASES.items():
        if re.search(r'\b' + alias + r'\b', low):
            return abbr
    return None


def mark_workout_done(day_abbr: str) -> bool:
    """Ставит ✅ для указанного дня в таблице тренировок goals.md. Возвращает True если изменение сделано."""
    path = MEMORY_PATH / "compiled" / "goals.md"
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    # Заменяем ❌ на ✅ только в строке с нужным днём
    pattern = rf'(\|\s*{re.escape(day_abbr)}\s*\|[^|]+\|)\s*❌\s*(\|)'
    new_content = re.sub(pattern, r'\1 ✅ \2', content)
    if new_content == content:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


def read_compiled(filename: str) -> str:
    path = MEMORY_PATH / "compiled" / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_compiled(filename: str, content: str):
    path = MEMORY_PATH / "compiled" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
