# Анализ YouTube каналов

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-yt-channels

---

📀 [**ССЫЛКА НА ШАБЛОН**](https://drive.google.com/file/d/15MEbWObkzqnn6MBPadunk34SXF8SFPXZ/view?usp=sharing)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305410664-______________2025-03-24___21.15.29.png)

### 🔍 Что делает:

Этот шаблон собирает данные о YouTube-каналах, вытаскивает видео с каждого из них, а затем ежедневно обновляет статистику по просмотрам, лайкам, комментариям и т.д. Все данные сохраняются в базу Supabase для дальнейшего анализа. Подходит для мониторинга конкурентов, поиска трендовых идей и построения дашбордов.

### 💻 Сервисы и интеграции:

- **N8N** — как основной инструмент

- **Supabase** — как база данных для хранения результатов (используется API и Postgres)

- **Google Cloud Console** — для получения API-ключа (**YouTube Data API v3** — для получения информации о каналах и видео)

## ⚙️ Установка и настройка

1. **Подключи Supabase и Google Cloud**
  - Для `YouTube Data API v3`:
  - Name: `key`
  - Value: `твой_API_ключ`

1. **Замути таблицы в Supabase**
  - `youtube_statistic_channels`
  - `youtube_statistic_videos`
  - `youtube_statistic_video_stat`
_(их шаблоны ниже)_

1. **Протестируй три воркфлоу вручную**
  - Сначала добавь канал через форму
  - Затем протестируй извлечение видео и статистики
  - После этого можешь переделать шаблон под свои задачи

### 1. API-ключи 🔑

- **Supabase**:

[https://supabase.com/](https://supabase.com/)

Зайди в Supabase → **Project Settings** → **Data API**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305411731-______________2025-03-24___18.17.52.png)

Скопируй **Project URL** и **Service Role ключ**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305412109-______________2025-03-24___18.19.23.png)

**Вставь их в N8N**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305412549-______________2025-03-24___18.23.39.png)

### ✅ Готово! Перейдём к следующему подключению.

- **Postgress**:

Тут всё тоже происходит внутри Supabase.

Зайди в Supabase → **Database**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305412954-______________2025-03-24___18.32.26.png)

Здесь мы возьмем пароль для подключения,

но сначала нажми на **Connect** наверху

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305413573-______________2025-03-24___18.33.33.png)

Здесь нас интересует _*Transaction pooler"_

на первой страницу внизу

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305414173-______________2025-03-24___18.34.39.png)

Если **нажать на стрелку вниз,** откроются нужные нам данные, которые необходимо **воткнуть сюда:**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305414711-______________2025-03-24___18.35.26.png)

**Но ещё нужен пароль.** Для этого вернёмся назад.

**Database Settings > Database password > Reset database password.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305415034-______________2025-03-24___18.37.38.png)

Тут есть прекрасная кнопка **Generate a password** которая сгенерирует нам пароль. После этого нажимаем **Сopy** и затем **Rest password** чтобы всё сохранилось. Скопированный пароль вставлем в N8N.

_Если после, этого вылезет ошибка подключения, но ты глазами видишь что все настроено правильно, можно её пока проигнорировать, потому что ошибка может появиться из-за отсутствия в твоей базе данных Supabase нужной таблицы. В следующих шага мы настроим таблицы, и затем ты сможешь протестировать подключение нормально._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305415558-______________2025-03-24___18.49.38.png)

### ✅ Отлично! Осталось подключить Google.

- **Google Cloude Console**:

[https://console.cloud.google.com](https://console.cloud.google.com/)

Зайди в **Console**, нажми на **три полоски** наверху слева чтобы открыть меню. И выбери здесь **APIs & Services→ Library.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305415910-______________2025-03-24___19.02.25.png)

Вбей в поиск: **YouTube Data API v3.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305416287-______________2025-03-24___19.05.22.png)

Открой, нажми на кнопку **ENABLE** и ты попадешь в раздел подключений.

**Credentials → + Create credentials → API key**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305416754-______________2025-03-24___19.07.47.png)

**Дождись создания ключа и скопируй его.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305417110-______________2025-03-24___19.10.38.png)

**Теперь воткнём его в N8N.**

Способ подключения не стандартный. Рассмотрим его на примере этого узла:

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305417485-______________2025-03-24___20.20.38.png)

**Query Auth → + Create new credential**

В **Name** → вставляем **key**

А в **Value** → **пароль** из Google Console

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305417889-______________2025-03-24___20.21.21.png)

### ✅ Save! С подключениями разобрались.

## 2. 🧮 База данных Supabase

- **Знакомство с функционалом:**

Слева в меню есть раздел **Table Editor,** в котором мы можем посмотреть таблицы, использующиеся для хранения информации в базе данных.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305418203-______________2025-03-24___19.47.10.png)

Таблицы можно создать вручную, но нам эта возня не нужна.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305418665-______________2025-03-24___19.48.10.png)

Вместо этого мы идем в **SQL Editor** чтобы создать их автоматически.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305419176-______________2025-03-24___19.51.02.png)

- **Что будем создавать:**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305419735-______________2025-03-24___19.53.47.png)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305420166-______________2025-03-24___19.54.34.png)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305420584-______________2025-03-24___19.55.45.png)

- **Код для SQL Editor** 🧩

**Вставляем ко**д, который я дам ниже

Нажимаем **Run**

При результате видим: _Success. Now rows returned_

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305420994-______________2025-03-24___19.58.15.png)

***Копируем всё → смело удаляем → вставляем новый код***

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-channels/1767305421448-______________2025-03-24___20.02.32.png)

### Что копировать:

🧩 **youtube_statistic_channels**:

```text
CREATE TABLE public.youtube_statistic_channels (
  id BIGSERIAL PRIMARY KEY,
  channel_handle TEXT,
  channel_id TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

```

🧩 **youtube_statistic_video_stat:**

```text
CREATE TABLE public.youtube_statistic_video_stat (
  id SERIAL PRIMARY KEY,
  video_id VARCHAR,
  view_count BIGINT,
  like_count BIGINT,
  favorite_count BIGINT,
  comment_count BIGINT,
  recorded_at TIMESTAMP
);

```

🧩 **youtube_statistic_videos:**

```text
CREATE TABLE public.youtube_statistic_videos (
  id VARCHAR PRIMARY KEY,
  kind VARCHAR,
  etag VARCHAR,
  published_at TIMESTAMP,
  channel_id VARCHAR,
  channel_title VARCHAR,
  title VARCHAR,
  description TEXT,
  category_id VARCHAR,
  live_broadcast_content VARCHAR,
  default_audio_language VARCHAR,
  thumbnail TEXT,
  tags JSONB,
  localized JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

```

## ▶️ Можно тестировать

Мы настроили автоматизацю для мониторинга YouTube-каналов от канала ИИздец. Она сохраняет нужные каналы, извлекает новые видео, собирает статистику и обновляет базу данных Supabase в реальном времени. Полученные данные можно использовать для: аналитики, транскрипции видео конкурентов, генерации идей итд.

## 🚨 Частые вопросы

**❓ Что делать, если API ключ не работает?**

➡️ Убедись, что:

- Ты включил **YouTube Data API v3** в Google Cloud Console

- Ключ скопирован без пробелов и вставлен в поле `key`

- Нет ограничений по IP или API в настройках ключа

**❓ Как проверить, что всё работает?**

➡️ Добавь любой канал через форму и проверь таблицы в Supabase:

- `youtube_statistic_channels` — появился канал?

- `youtube_statistic_videos` — подтянулись видео?

- `youtube_statistic_video_stat` — обновляется статистика?

**❓ Сколько видео подтягивается с одного канала?**

➡️ До **50 последних видео** на один вызов. Если хочешь больше — нужно внедрять пагинацию через `nextPageToken`.

**❓ Как можно использовать эти данные?**

➡️ Как хочешь:

- Отслеживать рост каналов и видео

- Выявлять тренды и форматы, которые "зашли"

- Делать внутренние отчёты по конкурентам

- Подбирать темы для своих видео

**❓ Можно ли получить текст из видео (транскрибацию)?**

➡️ Можно. Это тема другого урока. Ты берёшь `video_id`, строишь ссылку `https://youtube.com/watch?v={{id}}` и:

- Прогоняешь через **Whisper** или **YouTube Transcript API**

- Или делаешь **саммари** через ChatGPT по заголовку, описанию и метаданным

**❓ Можно ли встроить это в Telegram-бота?**

➡️ Легко. Пара шагов и у тебя:

- Мониторинг конкурентов

- Уведомления о новых видео

- Автогенерация идей и подборок

- 

**❓ Можно ли сделать красивую статистику (дашборд)?**

➡️ Конечно. Supabase интегрируется с:

- _Retool_

- _Metabase_

- _Notion_

- _Даже Google Data Studio_

**❓ Это всё бесплатно?**

➡️ N8N — опенсорсный проект

➡️ Supabase — бесплатен на старте

➡️ YouTube API — бесплатно до 10 000 юнитов/сутки (этого хватит с головой)
