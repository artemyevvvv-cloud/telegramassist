import io
import logging
import os
from pathlib import Path
from groq import Groq
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from memory import read_context, append_to_log, update_streak

logger = logging.getLogger(__name__)

ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"
KB_PATH = Path(os.environ.get("KB_PATH", str(Path(__file__).parent.parent.parent / "knowledge-base" / "aizdec")))

SYSTEM_PROMPT = """Ты личный ассистент. Ты знаешь историю пользователя и помогаешь отслеживать прогресс в обучении вайбкодингу и личные цели. Отвечай кратко и по делу. Говори на русском.

Контекст о пользователе:
{context}

{kb_section}"""


def search_kb(query: str, max_results: int = 2) -> str:
    """Ищет релевантные уроки в knowledge-base и возвращает их контент."""
    if not KB_PATH.exists():
        return ""
    words = [w.lower() for w in query.split() if len(w) > 2]
    if not words:
        return ""

    scored = []
    for path in KB_PATH.rglob("*.md"):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        score = sum(text.lower().count(w) for w in words)
        if score > 0:
            scored.append((score, text))

    scored.sort(reverse=True)
    top = scored[:max_results]
    if not top:
        return ""

    parts = ["=== Материалы из базы знаний курсов ==="]
    for _, content in top:
        parts.append(content[:1500].strip())
        parts.append("---")
    return "\n".join(parts)

MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Прогресс"), KeyboardButton("📅 План")],
        [KeyboardButton("🔥 Стрик"), KeyboardButton("✅ Стрик +1")],
        [KeyboardButton("🧠 Запомнить"), KeyboardButton("🗑️ Забыть")],
        [KeyboardButton("📚 Курсы")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)

COURSE_NAMES = {
    "claude-code":       "Claude Code",
    "publish":           "Публикация проекта",
    "n8n-mcp":           "N8N + Claude Code",
    "tuning-claude-code": "Тюнинг Claude",
    "constructor":       "Constructor (бета)",
}

MAX_MSG = 3800


def _lesson_title(path: Path) -> str:
    try:
        first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
        return first.lstrip("# ").strip()
    except Exception:
        return path.stem


def kb_courses_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for slug, name in COURSE_NAMES.items():
        course_dir = KB_PATH / slug
        if course_dir.exists():
            count = len(list(course_dir.glob("*.md")))
            buttons.append([InlineKeyboardButton(f"{name} ({count})", callback_data=f"kb_ls:{slug}")])
    return InlineKeyboardMarkup(buttons)


def kb_lessons_keyboard(course: str) -> InlineKeyboardMarkup:
    course_dir = KB_PATH / course
    buttons = []
    for f in sorted(course_dir.glob("*.md")):
        title = _lesson_title(f)
        slug = f.stem
        cb = f"kb_rd:{course}:{slug}"
        if len(cb.encode()) <= 64:
            buttons.append([InlineKeyboardButton(title, callback_data=cb)])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="kb_courses")])
    return InlineKeyboardMarkup(buttons)


def kb_lesson_keyboard(course: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("⬅️ Назад к урокам", callback_data=f"kb_ls:{course}")
    ]])


def is_allowed(update: Update) -> bool:
    return update.effective_user.id == ALLOWED_USER_ID


def ask_groq(user_message: str) -> str:
    ctx = read_context()
    kb = search_kb(user_message)
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=ctx, kb_section=kb)},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


async def _reply_md(update: Update, text: str, **kwargs):
    """Отправляет ответ с Markdown, при ошибке парсинга — plain text."""
    try:
        await update.message.reply_text(text, parse_mode="Markdown", **kwargs)
    except Exception:
        await update.message.reply_text(text, **kwargs)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(
        "Привет! Выбери действие из меню или просто напиши сообщение.",
        reply_markup=MENU,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        logger.warning("Blocked user %s", update.effective_user.id)
        return

    text = update.message.text
    try:
        awaiting = context.user_data.get("awaiting")

        if awaiting == "remember":
            context.user_data.pop("awaiting")
            append_to_log(f"**Запомнить:** {text}")
            await update.message.reply_text(f"Запомнил: {text}", reply_markup=MENU)
            return

        if awaiting == "forget":
            context.user_data.pop("awaiting")
            append_to_log(f"**Удалить из памяти:** {text}")
            await update.message.reply_text(
                f"Отметил для удаления: {text}\nПримени при следующей компиляции памяти.",
                reply_markup=MENU,
            )
            return

        if text == "📚 Курсы":
            append_to_log("**Кнопка:** 📚 Курсы")
            await update.message.reply_text(
                "Выбери курс:",
                reply_markup=kb_courses_keyboard(),
            )
            return

        if text == "📊 Прогресс":
            reply = ask_groq(
                "Покажи мой текущий прогресс по вайбкодингу: что пройдено, streak, оценки понимания."
            )
            append_to_log(f"**Кнопка:** 📊 Прогресс\n**Bot:** {reply}")
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "📅 План":
            reply = ask_groq(
                "Помоги составить план на сегодня с учётом моих целей и прогресса в учёбе."
            )
            append_to_log(f"**Кнопка:** 📅 План\n**Bot:** {reply}")
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "🔥 Стрик":
            reply = ask_groq(
                "Посчитай мой текущий streak по логам: сколько дней подряд я занимался? "
                "Считай строки '**Стрик:** день учёбы засчитан' и записи об учёбе в логах."
            )
            append_to_log(f"**Кнопка:** 🔥 Стрик\n**Bot:** {reply}")
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "✅ Стрик +1":
            update_streak()
            append_to_log("**Стрик:** день учёбы засчитан ✅")
            await update.message.reply_text("День засчитан! Стрик продолжается 🔥", reply_markup=MENU)
            return

        if text == "🧠 Запомнить":
            context.user_data["awaiting"] = "remember"
            await update.message.reply_text("Что запомнить?", reply_markup=MENU)
            return

        if text == "🗑️ Забыть":
            context.user_data["awaiting"] = "forget"
            await update.message.reply_text("Что забыть?", reply_markup=MENU)
            return

        reply = ask_groq(text)
        append_to_log(f"**User:** {text}\n**Bot:** {reply}")
        await _reply_md(update, reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_message: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=MENU)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.from_user.id != ALLOWED_USER_ID:
        return
    await query.answer()
    data = query.data

    if data == "kb_courses":
        await query.edit_message_text("Выбери курс:", reply_markup=kb_courses_keyboard())

    elif data.startswith("kb_ls:"):
        course = data[len("kb_ls:"):]
        name = COURSE_NAMES.get(course, course)
        await query.edit_message_text(
            f"📖 {name}\n\nВыбери урок:",
            reply_markup=kb_lessons_keyboard(course),
        )

    elif data.startswith("kb_rd:"):
        _, course, slug = data.split(":", 2)
        path = KB_PATH / course / f"{slug}.md"
        if not path.exists():
            await query.edit_message_text("⚠️ Урок не найден.", reply_markup=kb_lesson_keyboard(course))
            return
        content = path.read_text(encoding="utf-8", errors="ignore")

        chunks = []
        current = []
        current_len = 0
        for line in content.splitlines(keepends=True):
            if current_len + len(line) > MAX_MSG and current:
                chunks.append("".join(current))
                current = []
                current_len = 0
            current.append(line)
            current_len += len(line)
        if current:
            chunks.append("".join(current))

        await query.edit_message_text(
            chunks[0],
            reply_markup=None if len(chunks) > 1 else kb_lesson_keyboard(course),
            parse_mode="Markdown",
        )
        for i, chunk in enumerate(chunks[1:], start=1):
            is_last = (i == len(chunks) - 1)
            await query.message.reply_text(
                chunk,
                reply_markup=kb_lesson_keyboard(course) if is_last else None,
                parse_mode="Markdown",
            )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    try:
        await update.message.reply_text("🎤 Слушаю...", reply_markup=MENU)

        voice_file = await context.bot.get_file(update.message.voice.file_id)
        buf = io.BytesIO()
        await voice_file.download_to_memory(buf)
        buf.seek(0)

        transcription = groq_client.audio.transcriptions.create(
            file=("voice.ogg", buf.read()),
            model="whisper-large-v3-turbo",
            language="ru",
        )
        text = transcription.text

        await update.message.reply_text(f"🗣️ {text}", reply_markup=MENU)

        reply = ask_groq(text)
        append_to_log(f"**Voice:** {text}\n**Bot:** {reply}")
        await _reply_md(update, reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_voice: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка голосового: {e}", reply_markup=MENU)
