# Plan: Dashboard — Telegram Mini App

**Дата:** 2026-06-12  
**Спек:** `docs/superpowers/specs/2026-06-12-dashboard-design.md`  
**Статус:** Ready to implement

---

## Обзор

5 фаз. Можно реализовать линейно — каждая фаза завершена и проверена перед следующей.

```
Phase 1: GitHub remote + PAT        ~15 мин
Phase 2: dashboard/ — 3 файла      ~2-3 ч
Phase 3: Bot — кнопки push и WebApp ~30 мин
Phase 4: Vercel деплой              ~15 мин
Phase 5: BotFather Mini App         ~10 мин
```

---

## Phase 1: GitHub репозиторий

**Цель:** публичный репо с правильным remote, чтобы бот мог делать git push.

### 1.1 Создать репозиторий на GitHub
- Зайти на github.com → New repository
- Название: `telegramassist`
- Видимость: **Public** (нужно для raw.githubusercontent.com)
- README: не создавать (у нас уже есть)

### 1.2 Подключить remote
```bash
git remote add origin https://github.com/<username>/telegramassist.git
git branch -M main
git push -u origin main
```

### 1.3 Personal Access Token для бота
- GitHub → Settings → Developer settings → Personal access tokens → Fine-grained
- Repository: `telegramassist`
- Permissions: `Contents` → Read and write
- Скопировать токен

### 1.4 Добавить в .env
```env
GITHUB_TOKEN=ghp_...
GITHUB_REPO_URL=https://<username>:<token>@github.com/<username>/telegramassist.git
```

### 1.5 Настроить remote с токеном (один раз)
```bash
git remote set-url origin https://<username>:<token>@github.com/<username>/telegramassist.git
```

**Проверка:** `git push` работает без ввода пароля.

---

## Phase 2: Dashboard — три файла

Все файлы в папке `dashboard/`.

### 2.1 `dashboard/index.html`

Структура:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Viewport, charset -->
  <!-- Google Fonts: Space Grotesk + Space Mono + Inter -->
  <!-- Telegram WebApp SDK: https://telegram.org/js/telegram-web-app.js -->
  <!-- style.css -->
</head>
<body>
  <!-- Экран загрузки: спиннер -->
  <!-- Главный экран: 3 карточки -->
  <!--   Карточка #learning -->
  <!--   Карточка #workouts -->
  <!--   Карточка #work -->
  <!-- Детальный вид (overlay) -->
  <!-- app.js -->
</body>
</html>
```

Карточка — минимальная разметка:
```html
<div class="card" data-section="learning">
  <div class="card-icon"><!-- SVG иконка --></div>
  <div class="card-title">Учёба</div>
  <div class="card-metric" id="learning-metric">…</div>
  <div class="progress-bar"><div class="progress-fill" id="learning-progress"></div></div>
  <div class="card-status" id="learning-status">…</div>
</div>
```

SVG иконки (Lucide):
- Учёба: `BookOpen`
- Тренировки: `Dumbbell`
- Работа: `Briefcase`

### 2.2 `dashboard/style.css`

CSS-переменные из дизайн-системы:
```css
:root {
  --bg: #0F172A;
  --card-bg: #1E293B;
  --border: #334155;
  --accent-green: #22C55E;
  --accent-neon: #6366F1;
  --text: #F8FAFC;
  --text-muted: #94A3B8;
  --font-head: 'Space Grotesk', sans-serif;
  --font-mono: 'Space Mono', monospace;
  --font-body: 'Inter', sans-serif;
}
```

Ключевые стили:
- `body` — bg `#0F172A`, цвет `#F8FAFC`, font Inter
- `.cards-grid` — `display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px`
- `.card` — bg `#1E293B`, border `1px solid #334155`, border-radius 12px, cursor pointer
- `.card:hover` — border-color `#6366F1`, box-shadow neon glow
- `.progress-bar` — bg `#334155`, height 4px, border-radius 2px
- `.progress-fill` — bg `#22C55E`, transition width 300ms
- `.card-metric` — font-family `Space Mono`, font-size 24px
- Детальный вид `.detail-overlay` — position fixed, полный экран, bg `#0F172A`, z-index 100

Responsive:
```css
@media (max-width: 480px) {
  .cards-grid { grid-template-columns: 1fr; }
}
```

`prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
```

### 2.3 `dashboard/app.js`

**Конфигурация (вверху файла):**
```js
const GITHUB_RAW = 'https://raw.githubusercontent.com/<username>/telegramassist/main';
const FILES = {
  learning: `${GITHUB_RAW}/memory/compiled/learning.md`,
  goals:    `${GITHUB_RAW}/memory/compiled/goals.md`,
};
```

**Функции:**

`fetchMarkdown(url)` → Promise<string>
- fetch(url), fallback текст при ошибке

`parseStreak(md)` → `{ streak: number, lastDate: string }`
- regex `Текущий: (\d+) дней подряд`

`parseModules(md)` → `{ total: number, done: number, inProgress: string }`
- считает строки с ✅ / 🔶 / ⬜

`parseWorkouts(md)` → `{ weekDone: number, weekTotal: number, rows: Array, plan: string[] }`
- парсит таблицу `| День | Упражнение | Выполнено |`
- парсит секцию `### План от тренера`

`parseWork(md)` → `{ tasks: Array<{text,done}>, goals: Array<{text,done}> }`
- парсит `- [ ] / - [x]` списки в секциях `### Задачи` и `### Цели`

`renderCards(data)` → DOM update
- Заполняет `.card-metric`, `.progress-fill`, `.card-status` для каждой карточки

`renderDetail(section, data)` → DOM update
- Раскрывает `.detail-overlay` с полным содержимым секции

**Инициализация:**
```js
document.addEventListener('DOMContentLoaded', async () => {
  if (window.Telegram?.WebApp) Telegram.WebApp.ready();
  
  showLoading();
  const [learningMd, goalsMd] = await Promise.all([
    fetchMarkdown(FILES.learning),
    fetchMarkdown(FILES.goals),
  ]);
  
  const data = {
    learning: { ...parseStreak(learningMd), ...parseModules(learningMd) },
    workouts: parseWorkouts(goalsMd),
    work: parseWork(goalsMd),
  };
  
  hideLoading();
  renderCards(data);
  
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => renderDetail(card.dataset.section, data));
  });
});
```

**Обработка ошибок:**
- `fetchMarkdown` возвращает пустую строку при сетевой ошибке
- `parseXxx` возвращают дефолтные значения при пустом вводе
- Карточки показывают "Нет данных" вместо краша

---

## Phase 3: Bot — новые кнопки

### 3.1 Кнопка "🚀 Обновить дашборд"

В `src/bot/handlers.py`:

Добавить `import subprocess` вверху.

Добавить в `MENU` кнопку:
```python
MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Прогресс"), KeyboardButton("📅 План")],
        [KeyboardButton("🔥 Стрик"), KeyboardButton("✅ Стрик +1")],
        [KeyboardButton("🧠 Запомнить"), KeyboardButton("🗑️ Забыть")],
        [KeyboardButton("📚 Курсы"), KeyboardButton("🚀 Обновить дашборд")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)
```

Добавить обработчик в `handle_message`:
```python
if text == "🚀 Обновить дашборд":
    append_to_log("**Кнопка:** 🚀 Обновить дашборд")
    await update.message.reply_text("⏳ Публикую на GitHub...")
    try:
        repo_url = os.environ.get("GITHUB_REPO_URL", "")
        result = subprocess.run(
            ["git", "-C", "/app", "add", "memory/"],
            capture_output=True, text=True, timeout=30,
        )
        result = subprocess.run(
            ["git", "-C", "/app", "commit", "-m", "update memory [auto]", "--allow-empty"],
            capture_output=True, text=True, timeout=30,
        )
        result = subprocess.run(
            ["git", "-C", "/app", "push"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            await update.message.reply_text("Дашборд обновлён ✅", reply_markup=MENU)
        else:
            await update.message.reply_text(f"⚠️ Ошибка push:\n{result.stderr[:500]}", reply_markup=MENU)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=MENU)
    return
```

### 3.2 Кнопка "📊 Дашборд" (открывает Mini App)

После получения URL от Vercel добавить в `MENU` или отдельным inline:
```python
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "")

# В cmd_start или отдельном хэндлере:
web_app_button = InlineKeyboardButton(
    "📊 Открыть дашборд",
    web_app=WebAppInfo(url=DASHBOARD_URL)
)
```

Добавить в `.env`:
```env
DASHBOARD_URL=https://telegramassist.vercel.app
```

---

## Phase 4: Vercel деплой

### 4.1 Создать `vercel.json` (опционально)
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### 4.2 Задеплоить через Vercel CLI или UI
```bash
cd dashboard
npx vercel --prod
```

Или: vercel.com → New Project → Import Git repository → выбрать `telegramassist` → Root Directory: `dashboard`.

### 4.3 Проверить
- Открыть полученный URL в браузере
- Убедиться что данные загружаются из GitHub
- Проверить на мобильном

---

## Phase 5: BotFather — Mini App

1. Написать `@BotFather` → `/mybots`
2. Выбрать бота
3. `Bot Settings` → `Menu Button` → `Configure menu button`
4. Ввести URL: `https://telegramassist.vercel.app`
5. Ввести текст кнопки: `Dashboard`

**Проверка:** кнопка ☰ (или 4 квадрата) в интерфейсе бота открывает Mini App.

---

## Порядок реализации

```
1. Phase 1 (GitHub) — без этого ничего не работает
2. Phase 2 (dashboard/) — основная работа
3. Phase 4 (Vercel) — деплой сразу после dashboard/
4. Phase 3 (bot buttons) — после получения Vercel URL
5. Phase 5 (BotFather) — финальный шаг
```

---

## Файлы, которые будут созданы/изменены

| Файл | Действие |
|------|---------|
| `dashboard/index.html` | Создать |
| `dashboard/style.css` | Создать |
| `dashboard/app.js` | Создать |
| `vercel.json` | Создать (опционально) |
| `src/bot/handlers.py` | Изменить: добавить кнопку push + WebApp |
| `.env` | Изменить: добавить GITHUB_TOKEN, GITHUB_REPO_URL, DASHBOARD_URL |
| `docker-compose.yml` | Изменить: пробросить git config в контейнер |

---

## Зависимости и риски

| Риск | Митигация |
|------|-----------|
| git push из контейнера требует git установленного в образе | Добавить `RUN apt-get install -y git` в Dockerfile бота |
| git config (user.email, user.name) в контейнере | Добавить в Dockerfile или через env |
| raw.githubusercontent.com rate limit (анонимные запросы) | Дашборд открывается редко, нет проблем |
| goals.md пустой/с placeholder | parseWorkouts/parseWork возвращают дефолты, карточки показывают "Нет данных" |
| Telegram Mini App требует HTTPS | Vercel даёт HTTPS бесплатно |
