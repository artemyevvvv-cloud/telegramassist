import os
from datetime import time
from groq import Groq
from telegram.ext import Application
from memory import read_context

ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])
MORNING_HOUR = int(os.environ.get("MORNING_HOUR", 9))
EVENING_HOUR = int(os.environ.get("EVENING_HOUR", 21))

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


async def _send(context, prompt: str):
    ctx = read_context()
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Ты личный ассистент. Контекст о пользователе:\n{ctx}"},
            {"role": "user", "content": prompt},
        ],
    )
    text = response.choices[0].message.content
    await context.bot.send_message(chat_id=ALLOWED_USER_ID, text=text)


async def send_morning(context):
    await _send(
        context,
        "Напиши короткое утреннее приветствие: что я изучал вчера и один конкретный шаг на сегодня.",
    )


async def send_evening(context):
    await _send(
        context,
        "Напиши короткий вечерний вопрос: как прошёл день, что удалось сделать по учёбе?",
    )


def setup_scheduler(app: Application):
    job_queue = app.job_queue
    job_queue.run_daily(send_morning, time=time(hour=MORNING_HOUR, minute=0))
    job_queue.run_daily(send_evening, time=time(hour=EVENING_HOUR, minute=0))
