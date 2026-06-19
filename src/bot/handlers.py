import io
import logging
import os
import subprocess
from pathlib import Path
from groq import Groq
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from memory import read_context, append_to_log, update_streak, detect_workout_day, mark_workout_done, detect_learning, detect_work
from db import init_db, log_message

init_db()

logger = logging.getLogger(__name__)

ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "")
GIT_ROOT = str(Path(__file__).resolve().parent.parent.parent)

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

def _build_menu() -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton("📊 Прогресс"), KeyboardButton("📅 План")],
        [KeyboardButton("🔥 Стрик"), KeyboardButton("✅ Стрик +1")],
        [KeyboardButton("🧠 Запомнить"), KeyboardButton("🗑️ Забыть")],
        [KeyboardButton("📚 Курсы"), KeyboardButton("🚀 Обновить дашборд")],
    ]
    if DASHBOARD_URL:
        rows.append([KeyboardButton("📱 Дашборд", web_app=WebAppInfo(url=DASHBOARD_URL))])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True, is_persistent=True)

MENU = _build_menu()

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


def _git_push(files: list[str], label: str):
    repo_url = os.environ.get("GITHUB_REPO_URL", "")
    if not repo_url:
        return
    try:
        subprocess.run(["git", "-C", GIT_ROOT, "add"] + files, check=True, capture_output=True)
        diff = subprocess.run(["git", "-C", GIT_ROOT, "diff", "--staged", "--quiet"], capture_output=True)
        if diff.returncode == 0:
            return  # нечего коммитить
        subprocess.run(["git", "-C", GIT_ROOT, "commit", "-m", f"bot: {label}"], check=True, capture_output=True)
        subprocess.run(["git", "-C", GIT_ROOT, "push", repo_url, "main"], check=True, capture_output=True)
    except Exception:
        logger.exception("Ошибка git push (%s)", label)


def is_allowed(update: Update) -> bool:
    return update.effective_user.id == ALLOWED_USER_ID


DEMO_SYSTEM_PROMPT = """Ты демо-версия персонального Telegram-бота ассистента для вайбкодинга.
Отвечай кратко, дружелюбно, на русском. Объясни что этот бот умеет делать для своего владельца.
Не придумывай личные данные пользователя — это демо без реальной памяти."""


def ask_groq(user_message: str, demo: bool = False) -> str:
    if demo:
        system = DEMO_SYSTEM_PROMPT
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ]
    else:
        ctx = read_context()
        kb = search_kb(user_message)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(context=ctx, kb_section=kb)},
            {"role": "user", "content": user_message},
        ]
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


VISITORS_LOG = Path(__file__).resolve().parent.parent.parent / "memory" / "raw" / "visitors.md"


def log_visitor(update: Update):
    user = update.effective_user
    uid = user.id
    username = f"@{user.username}" if user.username else "—"
    name = user.full_name or "—"
    timestamp = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
    VISITORS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(VISITORS_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n- {timestamp} | id: `{uid}` | {username} | {name}")
    log_message(uid, username, name, "visitor", "/start")


async def _reply_md(update: Update, text: str, **kwargs):
    """Отправляет ответ с Markdown, при ошибке парсинга — plain text."""
    try:
        await update.message.reply_text(text, parse_mode="Markdown", **kwargs)
    except Exception:
        await update.message.reply_text(text, **kwargs)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_allowed(update):
        log_visitor(update)
        name = user.first_name or user.username or "друг"
        await update.message.reply_text(
            f"👋 Привет, {name}! Это демо-версия персонального бота-ассистента для вайбкодинга.\n\n"
            "Можешь потыкать кнопки — покажу что умею 👇",
            reply_markup=MENU,
        )
        return
    log_message(user.id, user.username or "", user.full_name or "", "start", "/start")
    await update.message.reply_text(
        "Привет! Выбери действие из меню или просто напиши сообщение.",
        reply_markup=MENU,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    demo = not is_allowed(update)
    user = update.effective_user
    uname = user.username or ""
    fname = user.full_name or ""

    text = update.message.text
    try:
        awaiting = context.user_data.get("awaiting")

        if awaiting == "remember":
            context.user_data.pop("awaiting")
            if demo:
                await update.message.reply_text("🔒 Это демо — запись в память недоступна.", reply_markup=MENU)
                log_message(user.id, uname, fname, "demo", text, "🔒 demo blocked")
            else:
                append_to_log(f"**Запомнить:** {text}")
                reply_text = f"Запомнил: {text}"
                await update.message.reply_text(reply_text, reply_markup=MENU)
                log_message(user.id, uname, fname, "remember", text, reply_text)
            return

        if awaiting == "forget":
            context.user_data.pop("awaiting")
            if demo:
                await update.message.reply_text("🔒 Это демо — изменение памяти недоступно.", reply_markup=MENU)
                log_message(user.id, uname, fname, "demo", text, "🔒 demo blocked")
            else:
                append_to_log(f"**Удалить из памяти:** {text}")
                reply_text = f"Отметил для удаления: {text}\nПримени при следующей компиляции памяти."
                await update.message.reply_text(reply_text, reply_markup=MENU)
                log_message(user.id, uname, fname, "forget", text, reply_text)
            return

        if text == "🚀 Обновить дашборд":
            if demo:
                await update.message.reply_text("🔒 Это демо — обновление дашборда недоступно.", reply_markup=MENU)
                return
            append_to_log("**Кнопка:** 🚀 Обновить дашборд")
            repo_url = os.environ.get("GITHUB_REPO_URL", "")
            if not repo_url:
                await update.message.reply_text("⚠️ GITHUB_REPO_URL не настроен.", reply_markup=MENU)
                return
            try:
                subprocess.run(["git", "-C", GIT_ROOT, "add", "memory/"], check=True, capture_output=True)
                commit = subprocess.run(
                    ["git", "-C", GIT_ROOT, "commit", "-m", "bot: update memory"],
                    capture_output=True,
                )
                if commit.returncode not in (0, 1):
                    raise RuntimeError("git commit failed")
                subprocess.run(["git", "-C", GIT_ROOT, "push", repo_url, "main"], check=True, capture_output=True)
                await update.message.reply_text("✅ Дашборд обновлён — данные памяти отправлены на GitHub.", reply_markup=MENU)
            except Exception:
                logger.exception("Ошибка обновления дашборда")
                await update.message.reply_text("⚠️ Не удалось обновить дашборд. Проверь логи.", reply_markup=MENU)
            return

        if text == "📚 Курсы":
            append_to_log("**Кнопка:** 📚 Курсы")
            log_message(user.id, uname, fname, "button", "📚 Курсы")
            await update.message.reply_text(
                "Выбери курс:",
                reply_markup=kb_courses_keyboard(),
            )
            return

        if text == "📊 Прогресс":
            reply = ask_groq(
                "Покажи мой текущий прогресс по вайбкодингу: что пройдено, streak, оценки понимания.",
                demo=demo,
            )
            if not demo:
                append_to_log(f"**Кнопка:** 📊 Прогресс\n**Bot:** {reply}")
            log_message(user.id, uname, fname, "button" if not demo else "demo", "📊 Прогресс", reply)
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "📅 План":
            reply = ask_groq(
                "Помоги составить план на сегодня с учётом моих целей и прогресса в учёбе.",
                demo=demo,
            )
            if not demo:
                append_to_log(f"**Кнопка:** 📅 План\n**Bot:** {reply}")
            log_message(user.id, uname, fname, "button" if not demo else "demo", "📅 План", reply)
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "🔥 Стрик":
            reply = ask_groq(
                "Покажи мой текущий стрик из раздела ## Streak в learning.md: "
                "сколько дней подряд (поле 'Текущий: N дней подряд') и когда последний день учёбы. "
                "Если стрик 0 — скажи об этом и предложи нажать '✅ Стрик +1' чтобы начать.",
                demo=demo,
            )
            if not demo:
                append_to_log(f"**Кнопка:** 🔥 Стрик\n**Bot:** {reply}")
            log_message(user.id, uname, fname, "button" if not demo else "demo", "🔥 Стрик", reply)
            await _reply_md(update, reply, reply_markup=MENU)
            return

        if text == "✅ Стрик +1":
            if demo:
                await update.message.reply_text("🔒 Это демо — запись стрика недоступна.", reply_markup=MENU)
                log_message(user.id, uname, fname, "demo", "✅ Стрик +1", "🔒 demo blocked")
            else:
                update_streak()
                append_to_log("**Стрик:** день учёбы засчитан ✅")
                _git_push(["memory/compiled/learning.md", "memory/raw/"], "streak +1")
                await update.message.reply_text("День засчитан! Стрик продолжается 🔥", reply_markup=MENU)
                log_message(user.id, uname, fname, "button", "✅ Стрик +1", "День засчитан! 🔥")
            return

        if text == "🧠 Запомнить":
            context.user_data["awaiting"] = "remember"
            log_message(user.id, uname, fname, "button", "🧠 Запомнить")
            await update.message.reply_text("Что запомнить?", reply_markup=MENU)
            return

        if text == "🗑️ Забыть":
            context.user_data["awaiting"] = "forget"
            log_message(user.id, uname, fname, "button", "🗑️ Забыть")
            await update.message.reply_text("Что забыть?", reply_markup=MENU)
            return

        # Авто-отметка тренировки: детектируем день + факт выполнения
        if not demo:
            day = detect_workout_day(text)
            if day and mark_workout_done(day):
                append_to_log(f"**Тренировка:** {day} отмечена ✅")
                _git_push(["memory/compiled/goals.md", "memory/raw/"], f"mark workout {day} done")
                reply_text = f"✅ Тренировка в {day} отмечена в дашборде!"
                log_message(user.id, uname, fname, "workout", text, reply_text)
                await update.message.reply_text(reply_text, reply_markup=MENU)
                return

        reply = ask_groq(text, demo=demo)
        if not demo:
            append_to_log(f"**User:** {text}\n**Bot:** {reply}")
            push_files = ["memory/raw/"]
            if detect_learning(text):
                update_streak()
                push_files.append("memory/compiled/learning.md")
            if detect_work(text):
                push_files.append("memory/compiled/goals.md")
            _git_push(push_files, "auto sync")
        log_message(user.id, uname, fname, "message" if not demo else "demo", text, reply)
        await _reply_md(update, reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_message: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=MENU)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
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

        kb_first = None if len(chunks) > 1 else kb_lesson_keyboard(course)
        try:
            await query.edit_message_text(chunks[0], reply_markup=kb_first, parse_mode="Markdown")
        except Exception:
            await query.edit_message_text(chunks[0], reply_markup=kb_first)

        for i, chunk in enumerate(chunks[1:], start=1):
            is_last = (i == len(chunks) - 1)
            kb = kb_lesson_keyboard(course) if is_last else None
            try:
                await query.message.reply_text(chunk, reply_markup=kb, parse_mode="Markdown")
            except Exception:
                await query.message.reply_text(chunk, reply_markup=kb)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    demo = not is_allowed(update)
    user = update.effective_user
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

        if not demo:
            day = detect_workout_day(text)
            if day and mark_workout_done(day):
                append_to_log(f"**Тренировка (голос):** {day} отмечена ✅")
                _git_push(["memory/compiled/goals.md", "memory/raw/"], f"mark workout {day} done")
                reply_text = f"✅ Тренировка в {day} отмечена в дашборде!"
                log_message(user.id, user.username or "", user.full_name or "", "workout_voice", text, reply_text)
                await update.message.reply_text(reply_text, reply_markup=MENU)
                return

        reply = ask_groq(text, demo=demo)
        if not demo:
            append_to_log(f"**Voice:** {text}\n**Bot:** {reply}")
            push_files = ["memory/raw/"]
            if detect_learning(text):
                update_streak()
                push_files.append("memory/compiled/learning.md")
            if detect_work(text):
                push_files.append("memory/compiled/goals.md")
            _git_push(push_files, "auto sync voice")
        log_message(user.id, user.username or "", user.full_name or "", "voice" if not demo else "demo_voice", text, reply)
        await _reply_md(update, reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_voice: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка голосового: {e}", reply_markup=MENU)
