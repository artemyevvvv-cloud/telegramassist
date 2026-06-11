# Текст из YouTube видео

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-yt-transcript

---

📀 [**ССЫЛКА НА ШАБЛОН**](https://drive.google.com/file/d/1bopo3Pz6y4WWX1lkf5oFztph9PrqHnbn/view?usp=sharing)

📖 [**ССЫЛКА НА ТАБЛИЦУ**](https://docs.google.com/spreadsheets/d/1b9BH4R3Kn4Hyq07RQ5oVNmuSZd3WMHruISPvYHDrQA8/edit?usp=sharing)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301192000-______________2025-03-25___04.09.01.png)

### 🔍 Что делает:

Это продолжение [предыдущего](/courses/n8n-mcp/n8n-tpl-yt-channels) воркфлоу. Здесь мы автоматически, раз в день, получаем транскрипции (текстовые версии) видео, которые мы уже спарсили и загрузили в базу данных Supabase. Затем мы объединим это все в красивой ГуглТаблице, вот так:

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301193065-______________2025-03-25___04.19.14.png)

### 💻 Сервисы и интеграции:

- **SearchApi** — сервис для расшифровки Ютуб видео (Google Cloude не позволяет это норм делать). Здесь нам сразу дают 100 бесплатных запросов за регистрацию

- **Supabase** — вытаскиваем инфу из базы данных

- **Google Cloud Console** — для подключения к Google Sheets (Гугл Таблицам)

## ⚙️ Установка и настройка

1. **Добавь новую колонку в таблицу Supabase**

- Назови её `published_at`

- Тут мы будем помечать видео, на которые уже сделана транскрипция, чтобы не прогонять их еще раз, не тратить токены, и не делать дубликаты в таблице.*

- По умолчанию будет стоять значение = `false`

- А после обработки меняться на = `true`

- _(код для добавления внизу, не ссы :)_

1. **Создай таблицу в Google Sheets**

- Замути Credential через Google Cloude Console

- Открой [мою таблицу](https://docs.google.com/spreadsheets/d/1b9BH4R3Kn4Hyq07RQ5oVNmuSZd3WMHruISPvYHDrQA8/edit?usp=sharing) и скопируй её

- **Файл → Создать копию**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301194028-______________2025-03-25___05.56.49.png)

1. **Вставь ключ от SearchAPI в N8N**

### 1. Обновление таблицы в Supabase

**Щас покажу как изи обновлять таблицы:**

Заходим в уже знакомый нам **SQL Editor**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301194508-______________2025-03-25___04.25.17.png)

**Вставляем этот код  →  жмём Run**

```sql
ALTER TABLE youtube_statistic_videos
ADD COLUMN processed BOOLEAN DEFAULT false;

```

Генерить подобное можно в ChatGPT, он прекрасно понимает такие запросы.

### 2. Подключение Supabase

Делается как в предыдущем уроке.

В поле **Limits** пишется количество строк берущихся из Supabase.

Это все-таки база данных. Можно не стесняться.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301194985-______________2025-03-25___05.14.22.png)

### 3. Подключение Гугл Таблиц

Мутится через Google Console, супер-легко, я уже показывал как.

**Получится вот так:**

| **video_id** | **Title** | **Transcript** | **Summary** | **Views** | **Likes** | **Comments** | **Published** | **Created At** | **Status** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `done` |
|  |  |  |  |  |  |  |  |  |  |

- **Published** показывает дату публикации видео.

- **Created At** указывает дату когда в таблицу добавилась транскрипция.

- **Status** `done` проставляется когда всё прошло успешно.

**Важно:** если ты создашь новую таблицу, то при первом запуске шаблон будет выдавать ошибку. В таком случае, нужно завести эту колмагу с толкача. Вставь ссылку на что-нибудь, чтобы таблица не была пустой, и тогда всё будет работать.

## 4. Подключение SearchApi

**После регистрации скопируй API ключ на главной странице**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301195805-______________2025-03-25___06.12.22.png)

**Если чё в Search History можно будет смотреть историю запусков**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301196226-______________2025-03-25___06.12.44.png)

Теперь открой в шаблоне **Set Video ID**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301196575-______________2025-03-25___05.24.45.png)

**Не перепутай куда вставлять!**

Поле для ключа (**api key**)  →  _ВЫДЕЛИЛ КАПСОМ_

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301196949-______________2025-03-25___05.25.47.png)

Язык видео выставляется в (**lang**) → _en / ru_

Ну и всё, ключ будет подтягиваться автоматически куда надо.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301197320-______________2025-03-25___05.30.47.png)

## Ещё раз, что тут происходит:

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-yt-transcript/1767301197815-______________2025-03-25___04.09.01_1.png)

| **Этап** | **Описание** |
| --- | --- |
| 1. Supabase | Берём `video_id`, `title`, `published`, только если `processed = false` |
| 2. Google Sheets | Загружаем инфу из таблицы для проверки дубликатов |
| 3. Transcribe | Достаём текст через SearchAPI |
| 4. Process Transcripts | Чистим `[Музыка]`, удаляем шум |
| 5. Summary Agent | GPT-4 делает саммари |
| 6. Merge с Supabase2 | Подтягиваем статистику из БД (views, likes, comments) |
| 7. Update Row | Пишем всё в таблицу (summary, transcript, views, etc.) |
| 8. Processed True | Обновляем `processed = true` в Supabase |
|  |  |

### Шаблон запускается автоматически по тамеру 🔁 а обработанные видео снова в процесс не попадут.
