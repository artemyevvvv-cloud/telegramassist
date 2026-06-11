# N8N на Railway (старый способ)

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-railway-old

---

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301164432-telegram-cloud-photo-size-1-5168071333836336566-y.jpg)

Сейчас мы не только сэкономим $20 в месяц на подписке N8N благодаря Railway. Но и впихнем туда программу, которая нам нужна для создания видео-контента, что сэкономит дополнительные несколько десятков $.

**Примерное время установки:** 15-25 минут.

**Стоимость:** на _Railway_ рекомендуется Hobby Plan (_~$5/месяц_ + плата за ресурсы сверх лимита, но лимиты довольно щедрые, и не факт что будут тобой превышены).

## 💻 Сервисы и интеграции:

- [**Railway.com**](https://railway.com/) — облачная платформа, на которой можно разворачивать и запускать приложения без гемора, например N8N. Всё работает из коробки: ты загружаешь проект, и платформа сама запускает его, следит за работой и держит в онлайне 24/7. Это удобно, если ты не хочешь настраивать сервер вручную.

- [**GitHub**](https://github.com/) — сайт, где хранятся файлы проектов. Там лежат инструкции, код и всё, что нужно для запуска приложений, например N8N. Эти файлы называются "репозитории" (по сути, это просто папка с файлами).

- **FFmpeg** — прога, которая умеет монтировать видео. Она не имеет интерфейса как обычные видеоредакторы, типа CapCut или Adobe Premiere. Вместо этого мы управляем ей текстовыми командами.

## ⚙️ Установка и настройка

1. Регистрация и выбор тарифа

1. Подготовка "рецепта" N8N с FFmpeg

1. Развертывание сервисов на Railway

1. Настройка (переменных окружения)

1. Первый вход и проверка FFmpeg

## 1️⃣ Регистрация и выбор тарифа

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301164888-______________2025-04-07___02.23.46.png)

1. **Зайди на** [https://railway.com](https://railway.com/)

1. **Зарегистрируйся
**Нажми _"Login"_. Самый простой способ — использовать GitHub аккаунт (давно пора его сделать). Railway попросит дать доступ к твоим репозиториям (это нужно для развертывания).

1. **Перейди на Hobby Plan
**В настройках аккаунта _(кликни на свой аватар -> Account Settings -> Plans)_ выбери **Hobby Plan**. Он стоит $5 в месяц и дает гораздо больше ресурсов, чем бесплатный, плюс снимает некоторые ограничения. Пока что нам этого хватит.

### ✅ Аккаунт готов.

## 2️⃣ Подготовка "рецепта" N8N с FFmpeg

Railway удобнее всего разворачивает приложения из GitHub-репозиториев, особенно если нам нужно немного доработать Docker-образ. Проще говоря: щас мы сделаем файл-инструкцию, прочитав который Railway запустит нужные программы.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301165477-______________2025-04-05___23.49.41.png)

1. **Создай (импортируй) репозиторий на GitHub:**

- **Зайди** на [https://github.com/](https://github.com/).

- **Нажми** "+" в правом верхнем углу -> _"New repository"_.

- **Найди** там кнопку [Import a repository.](https://github.com/new/import)

- **Вставь** в _"The URL for your source repository"_ **вот эту ссылку:
**[https://github.com/thecrocoinc/n8n-railway-ffmpeg](https://github.com/thecrocoinc/n8n-railway-ffmpeg)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301165866-______________2025-04-07___02.34.01.png)

**Придумай названи**е и вставь его в _"Repository name"_

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301166217-______________2025-04-07___02.37.43.png)

**Begin Import**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301166571-______________2025-04-07___02.41.02.png)

Теперь ждём.

**Ты можешь также создать свой репозиторий с нуля****.**

**Для этого:**

- В созданном репозитории нажми -> "**Create new file**".

- Назови файл `**Dockerfile**` (именно так, с большой буквы, без расширения).

- Вставь в него следующий код:

```docker
FROM docker.n8n.io/n8nio/n8n:latest
USER root
RUN apk add --no-cache ffmpeg curl
RUN chown -R node:node /home/node/.n8n
USER node

```

**ЧТО ЭТО ДЕЛАЕТ:**

- `FROM ...`: Берет официальный образ n8n.

- `USER root`: Временно становится главным администратором внутри контейнера.

- `RUN apk add ...`: Устанавливает программы `ffmpeg` и `curl`.

- `RUN chown ...`: Убеждается, что у n8n есть права на свою папку.

- `USER node`: Возвращается к обычному пользователю n8n.

- Нажми **"Commit new file"**.

Теперь нажав на аватарку справа вверху и выбрав **Your repositories,** ты можешь посмотреть свои репозитории. Поздравляю!

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301166923-______________2025-04-07___02.42.36.png)

### ✅ Рецепт написан.

## 3️⃣ Развертывание сервисов на Railway

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301167373-______________2025-04-07___02.48.09.png)

1. **Создай проект на Railway:
**- Вернись в свою панель [Railway](https://railway.app/dashboard).
- Нажми "**+ New Project**".
- Выбери **"Deploy from GitHub repo"**.
- Настрой доступ к GitHub, если еще не сделал, и выбери _репозиторий с твоим названием_, который только что создал. Если файл не будет виден, попробуй обновить страницу, или даже удалить подключение GitHub и врубить его заново.
- Если все четко, Railway автоматически обнаружит `Dockerfile` и начнет сборку и развертывание сервиса N8N. Это может занять несколько минут.

1. **Добавь базу данных PostgreSQL:
**- Пока N8N разворачивается, нажми "**+ Create**" (внутри твоего проекта).
- Выбери "**Database**".
- Выбери "**Add PostgreSQL**". Railway создаст базу данных и покажет переменные для подключения к ней.

1. **Добавь Redis:
**- Снова нажми "**+ New**".
- Выбери "**Database**".
- Выбери "**Add Redis**".

**Теперь у тебя в проекте три сервиса:** _твой N8N, PostgreSQL и Redis._

### ✅ Проект запущен.

## 4️⃣ Настройка (переменных окружения)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301167747-______________2025-04-05___23.27.57.png)

1. Кликни на развёрнутый N8N `(у меня он назван n8n-on-railway)` в проекте.

1. Перейди на вкладку **"Variables"**.

1. **Добавь переменные** через кнопку **"+ New Variable"** вручную для каждой строки. То, что слева (до ":") копируешь из этой инструкции. То, что справа (в фигурных скобках) выбираешь из выпадающего списка.
- `DB_TYPE`: `postgresdb
`- `DB_POSTGRESDB_HOST`: **Используй переменную Railway!** Нажми. **"Show More"** и выбери `{{Postgres.PGHOST}}` из подсказок. Не вводи IP вручную!

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301168164-______________2025-04-05___23.30.26.png)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301168499-______________2025-04-05___23.31.59.png)

- `DB_POSTGRESDB_PORT`: аналогично, `{{Postgres.PGPORT}}`.

- `DB_POSTGRESDB_DATABASE`: аналогично, `{{Postgres.PGDATABASE}}`.

- `DB_POSTGRESDB_USER`: аналогично, `{{Postgres.PGUSER}}`.

- `DB_POSTGRESDB_PASSWORD`: аналогично, `{{Postgres.PGPASSWORD}}`.

- `N8N_HOST`: Сначала можешь вставить сюда **публичный домен**, который Railway предоставил твоему n8n-сервису.

Его можно найти во вкладке **Settings** -> **Networking** -> **Public Networking**. Он будет вида `n8n-railway-ffmpeg-production-XXXX.up.railway.app`. Если не появился, нажми сгенерировать. Немного позже ты сможешь привязать свой домен и обновить эту переменную.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301168888-______________2025-04-05___23.34.23.png)

- `WEBHOOK_URL`: `https://<тот_же_адрес_из_N8N_HOST>/`

( на место скобок < > вставь тот же домен, что копировал на предыдущем шаге, а в конце обязательно должна быть черточка `/` )

- `N8N_PROTOCOL`: `https`

- `EXECUTIONS_MODE`: `regular`

- `QUEUE_BULL_REDIS_HOST`: **Используй переменную Railway!** Выбери вручную, как делали с Postgress, только `$ {{Redis.REDISHOST}}`

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301169251-______________2025-04-05___23.37.41.png)

- `QUEUE_HEALTH_CHECK_ACTIVE`: `true`

- `N8N_ENCRYPTION_KEY`: СГЕНЕРИРУЙ НАДЕЖНЫЙ СЛУЧАЙНЫЙ КЛЮЧ! Используй менеджер паролей или онлайн-генератор. **Обязательно сохрани этот ключ в надежном месте!** Без него ты потеряешь доступ ко всем сохраненным кредам в N8N. Пример: `MySecretKey123!@#ButMakeItMuchLongerAndRandom`.

- `N8N_DEFAULT_BINARY_DATA_MODE`: `filesystem`

- `N8N_PAYLOAD_SIZE_MAX`: `512`

- `NODE_OPTIONS`: `-max-old-space-size=4096`

- `N8N_FILESYSTEM_MAX_SIZE`: `512`

- `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS`: `false`

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301169562-______________2025-04-07___02.53.50.png)

1. **Дождись переразвертывания:
**После добавления/изменения переменных Railway, нажми **Deploy** и _Railway_ автоматически переразвернет сервис **N8N** с новыми настройками. Следи за статусом во вкладке "Deployments".

### ✅ Настройка завершена.

## 5️⃣ Первый вход и проверка FFmpeg

1. **Открой n8n:
**Перейди по публичному адресу твоего n8n (который ты указал в `N8N_HOST`, вида `https://n8n-railway-ffmpeg-production-XXXX.up.railway.app`).

1. **Создай аккаунт владельца:
**Ты увидишь страницу настройки пользователя N8N. Задай email, имя, пароль.

1. **Проверь FFmpeg (Рекомендуется):
**- Создай новый пустой воркфлоу.
- Добавь узел `Execute Command`.
- В поле `Command` введи: `ffmpeg -version
`- Запусти узел.
- Во вкладке " O U T P U T" ты должен увидеть информацию о версии FFmpeg, а не ошибку "command not found". Если видишь версию – значит, FFmpeg успешно установлен в контейнере!

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-railway-old/1767301170064-______________2025-04-05___23.48.03.png)

### ✅ Красава!
