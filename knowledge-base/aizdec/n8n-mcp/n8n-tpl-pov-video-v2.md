# Фабрика POV видео (v1.2)

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-pov-video-v2

---

💽 [**ССЫЛКА НА ШАБЛОН**](https://drive.google.com/file/d/14zYZTEH_eyJbabq1yw9D0nNMCmPG8Y1D/view?usp=sharing)

📖 [**ССЫЛКА НА ТАБЛИЦУ**](https://docs.google.com/spreadsheets/d/1wOEb1nbNGNQUuKLclMstjvR6bFSDcCsrrZ_QGvs57-A/edit?usp=sharing)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301155931-______________2025-04-07___03.10.09.png)

Здарова! В одном из предыдущих уроков мы уже развернули N8N на своем сервере с FFmpeg (прогой для бесплатного монтажа). Теперь пора прокачать генератор POV видео 1.1 до **версии 1.2** – сделать его **дешевле, проще и эффективнее**.

### 🔍 Что нового в версии 1.2 :

1. **Бесплатный рендеринг
**Забываем про платный Creatomate. Наш N8N на Railway (или другом self-host) теперь сам монтирует видео с помощью FFmpeg. Экономим деньги, получаем полный контроль.

1. **Новый AI для картинок и видео (AI/ML API)
**Вместо PiAPI используем `api.aimlapi.com`. Его можно пополнять криптой.

1. **Качество стало лучше
**И всё уже адаптировано под русский текст, разумеется.

1. **Подготовка к мультипостингу
**Добавляем узлы для автозагрузки в TikTok и Instagram через сервис [Upload-Post.com](http://upload-post.com/).

**Твоя задача:**

Взять готовый шаблон 1.2, импортировать в свой N8N на Railway и подключить внешние сервисы. Промпты и скрипты уже настроены как надо (включая генерацию русских титров).

**Погнали!**

### 💻 Сервисы и интеграции:

- **N8N размещенный на Railway** — очень важно для этого шаблона

- **FFmpeg** — программа, из-за которой вся эта возня

- [**AI/ML API**](https://aimlapi.com/) — сервис для моделек генерации изображений и видео

- [**Upload-Post**](https://www.upload-post.com/) — для мультипостинга.

### ⚙️ Установка и настройка

1. Импорт и базовые подключения

1. Подключаем AI/ML API

1. Проверяем рендер через FFmpeg

1. Настройка мультипостинга

1. Запуск и проверка шаблона

## 1️⃣ Импорт и базовые подключения

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301156503-______________2025-04-07___03.18.17.png)

1. **Импортируй JSON-шаблон**

1. **Подключи сервисы**:

- **Google Sheets (таблицы)
**Ты уже знаешь как делать это через Google Cloude Console.
После подключения –> создай копию моей таблицы.
Открой её по [этой ссылке.
](https://docs.google.com/spreadsheets/d/1wOEb1nbNGNQUuKLclMstjvR6bFSDcCsrrZ_QGvs57-A/edit?usp=sharing)**Файл –> Создать копию.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301157004-______________2025-04-07___04.11.45.png)

- **Google Drive (диск)
**Скопируй OAuth Redirect URL и вставь его в Cloude Console при создании Credential. Важно чтобы адрес в N8N и Google был одинаковым.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301157504-______________2025-04-07___04.00.22.png)

- **GPT 4o
**Сделай это через OpenAI или OpenRouter. _Промпт агента уже настроен на генерацию русского _`_title_`_ и английских _`_prompt_`_/_`_sound_`_._ Это значит, что текст на видео будет на русском, а промты для генерации изображений и видео на английском. Все четко.

- **ElevenLabs
**Подключи API-ключ ElevenLabs через.

- **Google Drive
**Подключи свои Google Drive OAuth2 Credentials. В узле `Upload Mp3` выбери папку для аудио (ID папки из JSON: `1hbvDU...`).

### ✅ Со знакомыми подключениями разобрались.

## 2️⃣ Интегрируем AI/ML API

Генерация картинок и видео теперь идет через `api.aimlapi.com`. В предыдущем шаблоне мы использовали PiAPI, но не ограничиваться же одним инструментом! Гибкость – ключ к грамотным автоматизациям.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301158124-______________2025-04-06___23.58.21.png)

1. **Получи API Ключ:
**Зайди на сайт AI/ML API (если еще нет аккаунта), получи свой API ключ.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301159081-______________2025-04-07___03.25.56.png)

1. **Создай Credential в N8N:**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301159613-______________2025-04-07___03.29.07.png)

- Открой узел _Text to Image_ -> `+ Create new credential`.

- Назови понятно, например `AIML API`.

- `Name`: `Authorization`

- `Value`: `Bearer <ТВОЙ_AIML_API_КЛЮЧ>` (вставь свой ключ вместо `<...>`).

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301159960-______________2025-04-07___03.28.49.png)

**Подключи остальные узлы:**

- Открой `Image to video` и `Get Video`.

- В поле `Credentials` для `Header Auth` выбери уже созданное подключение `AIML API Creds`.

**О ТАРИФАХ:**

На сервисе есть тариф без подписки, с пополнением баланса на фиксированную сумму. Создание 7 изображений + 7 отрезков для одного видео мне обходится примерно в $1. Весьма экономично, учитывая адекватное качество и то, что стоимость всех моделек падает в несколько раз за год :)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301160423-______________2025-04-07___03.54.58.png)

### ✅ Генерацию контента настроили.

## 3️⃣ Проверяем рендер через FFmpeg

Монтаж теперь делает FFmpeg прямо на твоем сервере.

1. **Узел **`**Render Script
**`Содержит готовый JS-код, который формирует команду для FFmpeg (собирает видео, аудио, **русские титры** `title` из OpenAI, добавляет эффекты). _Ничего менять не нужно, если только не хочешь кастомизировать эффекты или шрифты._

1. **Узел **`**Render Execution**`** (Execute Command)
**Выполняет команду из `Render Script`. _Настройки (_`_{{ $json.command }}_`_) уже верные._

1. **Узел **`**Get Video from Disk**`** (Read File):
**Забирает готовое видео (`/tmp/n8n/final_output.mp4`) для дальнейшей загрузки.

### ✅ Изучи их и идём дальше.

## 4️⃣ Настройка мультипостинга

В этом шаблоне мы используем сервис `Upload-Post.com` для TikTok/Instagram. Он позволяет быстро запустить автопостинг в TikTok и Instagram без головной боли с их родными API, используя простой HTTP-запрос из N8N.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v2/1767301161560-______________2025-04-07___04.25.46.png)

1. **Получи API ключ на Upload-Post:
**Зарегистрируйся на `upload-post.com`, найди и скопируй свой API ключ.

1. **Создай + New Credential в N8N:
**- Тип: `Header Auth
`- `Credential Name`: `Upload Post
`- `Name`: `Authorization
`- `Value`: `Apikey <ТВОЙ_API_КЛЮЧ_UPLOAD_POST>` (вставь свой).
- Сохрани.

1. **Настрой узлы постинга:
**- `**YouTube
**`К нему подключаемся напрямую.
- `**TikTok**`** (HTTP Request)
**- `Credentials`: `Upload Post Creds
`- `Body Parameters`: проверь поля `title`, `platform[]` (`tiktok`), `video` (должно ссылаться на `data`), `user` (введи свой username с Upload-Post).
- `**Instagram**`** (HTTP Request)
**- `Credentials`: `Upload Post Creds
`- `Body Parameters`: аналогично TikTok, но `platform[]`: `instagram` и `user` (твой username с Upload-Post).

1. **Включи постинг:
**В JSON узлы `YouTube`, `TikTok`, `Instagram` и `Update google sheet` отключены потому что я использую немного другой способ публикации контента. Но тебе все равно рекомендую ознакомиться с тем, что представлено в этом шаблоне, чтобы дальше мы могли общаться на одном языке.

1. **Подключи выходы:
**Свяжи выход `Get Video from Disk` со входами `YouTube`, `TikTok`, `Instagram`.

### ✅ С публикацией видео разобрались.

## 5️⃣ Тестовый запуск

1. **Проверка
**Все нужные Credentials подключены? Узлы постинга и обновления таблицы **настроены**? В Google Sheets (таблице) есть идеи, которые агент может вытянуть?

1. **Тест
**Жми "Test workflow". Смотри, чтобы все шаги прошли без ошибок. Если что-то встало – копируй ошибку и вставляй в ChatGPT, желательно прикрепив шаблон и скриншот процесс. Чем больше вводных ты ему дашь, тем точнее будет ответ.

1. **Активация
**Если тест прошел, включай воркфлоу (переключатель `Active`) и настраивай `Schedule Trigger` (таймер) на удобный интервал. Теперь останется только заполнять таблицу с идеями, или создать под эту задачу отдельного агента.

### ✅ Генератор видео версии 1.2 готов.

Теперь ты можешь автоматизированно создавать видосы с русскими титрами, бесплатно их рендерить и раскидывать по соцсетям, не прикладывая к этому почти никаких усилий. Эффективно и экономно.
