# Tasks

## Приоритет 1 — Скелет проекта
- [ ] Создать структуру папок: `src/bot/`, `src/mcp/`, `memory/`, `memory/log/`
- [ ] Написать `docker-compose.yml` с тремя сервисами (telegram-bot, mcp-server, volume)
- [ ] Создать `memory/core.md`, `memory/learning.md`, `memory/goals.md` с начальным содержимым

## Приоритет 2 — MCP-сервер
- [ ] Реализовать FastMCP сервер с инструментами: `read_memory`, `write_memory`, `search_memory`
- [ ] Добавить `log_conversation` (запись в SQLite)
- [ ] Добавить `web_search` через DuckDuckGo API

## Приоритет 3 — Telegram-бот
- [ ] Настроить python-telegram-bot, получить токен от @BotFather
- [ ] Реализовать обработку обычных сообщений (читает память → Groq → ответ)
- [ ] Реализовать slash-команды: `/progress`, `/remember`, `/plan`, `/streak`, `/forget`

## Приоритет 4 — Деплой
- [ ] Выбрать VPS (открытый вопрос)
- [ ] Настроить git-деплой: `git pull && docker compose up -d`
- [ ] Настроить бэкап памяти в git (cron или хук)
