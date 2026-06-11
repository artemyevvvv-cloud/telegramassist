import io
import logging
import os
from pathlib import Path
from groq import Groq
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from memory import read_context, append_to_log

logger = logging.getLogger(__name__)

ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"
KB_PATH = Path(os.environ.get("KB_PATH", "./knowledge-base/aizdec"))

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
        # Берём первые 1500 символов чтобы не раздувать контекст
        parts.append(content[:1500].strip())
        parts.append("---")
    return "\n".join(parts)

MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Прогресс"), KeyboardButton("📅 План")],
        [KeyboardButton("🔥 Стрик"), KeyboardButton("✅ Стрик +1")],
        [KeyboardButton("🧠 Запомнить"), KeyboardButton("🗑️ Забыть")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


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

        if text == "📊 Прогресс":
            reply = ask_groq(
                "Покажи мой текущий прогресс по вайбкодингу: что пройдено, streak, оценки понимания."
            )
            await update.message.reply_text(reply, reply_markup=MENU)
            return

        if text == "📅 План":
            reply = ask_groq(
                "Помоги составить план на сегодня с учётом моих целей и прогресса в учёбе."
            )
            await update.message.reply_text(reply, reply_markup=MENU)
            return

        if text == "🔥 Стрик":
            reply = ask_groq(
                "Посчитай мой текущий streak по логам: сколько дней подряд я занимался? "
                "Считай строки '**Стрик:** день учёбы засчитан' и записи об учёбе в логах."
            )
            await update.message.reply_text(reply, reply_markup=MENU)
            return

        if text == "✅ Стрик +1":
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
        await update.message.reply_text(reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_message: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=MENU)


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
        await update.message.reply_text(reply, reply_markup=MENU)

    except Exception as e:
        logger.exception("Ошибка в handle_voice: %s", e)
        await update.message.reply_text(f"⚠️ Ошибка голосового: {e}", reply_markup=MENU)
