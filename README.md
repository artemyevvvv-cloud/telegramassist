# telegramassist

Персональный ИИ-ассистент в Telegram для отслеживания прогресса в обучении вайбкодингу и личных целей. Работает 24/7 на VPS, помнит всё между сессиями через markdown-файлы (метод Карпатого).

**Стек:** Python · python-telegram-bot · Groq API (Llama 3.3 70B) · FastMCP · Docker Compose

## Запуск

```bash
# Деплой на VPS
git pull && docker compose up -d
```

Требуется: Telegram Bot Token (от @BotFather), Groq API Key, VPS с Docker.
