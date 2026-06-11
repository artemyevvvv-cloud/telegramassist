# SMM сотрудники

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-smm-team

---

# 0. Открываем видео-инструкцию

_И действуем четко по ней, подглядывая в этот файл_ 👀

[https://youtu.be/VfWLQX9Ual8](https://youtu.be/VfWLQX9Ual8)

🔗 **Ссылка на шаблоны лежит в моем телеграм-канале.**

# 1. Устанавливаем кастомные ноды

**[A] Облачная версия N8N (n8n.cloud)**

**Просто вписать название в строку поиска нод:**

- scrapingbee

- [ Telegramify для это версии N8N нет ]

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301172302-Screenshot_2025-10-22_at_16.58.15.png)

**[B] На своем сервере (Railway или другой)**

**Settings > Community nodes (в конце)**

- n8n-nodes-scrapingbee

- n8n-nodes-telegramify-markdown

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301172681-Screenshot_2025-10-22_at_16.57.49.png)

# 2. Создаем проект в базе данных Supabase

_Это самая простая и удобная база данных для агентов._

[https://supabase.com/dashboard/organizations](https://supabase.com/dashboard/organizations)

1. Создаем проект (и ждем несколько минут)

1. Импортируем SQL код в **SQL-Editor** чтобы создать таблицы _(SQL код показан в видео-инструкции выше)_

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301173040-Screenshot_2025-10-22_at_23.39.59.png)

☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽☝🏽

1. **После этого открываем Project Settings и ищем поля, которые понадобятся нам для подключения проекта к N8N:**

**Data API** – тут юзернейм проекта после “https://” и до “.supabase”, и еще тут Host ссылка проекта, ее можно копировать целиком.
**API Keys** – тут service_role для обычной Supabase ноды.
**API Keys** – тут anon_public для HTTP ноды.

_**(а)**_** Обычная нода Supabase настраивается как в 🎥 видео-инструкции.**

_**(b)**_** Credential в http-ноде **_**“Load Reply Context (RPC)”**_** делается так:**

- Name: `Authorization`

- Value: `Bearer YOUR_API_KEY`

# 3. News Parser

### [1.1] Копируем таблицу Airtable

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301173441-Screenshot_2025-10-22_at_23.37.44.png)

_Это аналог Гугл-таблиц, который проще подключается._

https://airtable.com/app6YBO4m1oiBO7L2/shrrUSQiO1ggwvn09

### [1.2] Создаем “**Personal access token”**

https://airtable.com/create/tokens

### [1.3] Проверяем “Save to Processed”

**URL:
**{{ $json.articles?.source_url || $json.source_url }}
**ДАТА ОБРАБОТКИ:
**{{ $json.articles?.processed_at || $json.processed_at || $now() }}

### [2] Регаемся в ScrapingBee и копируем ключ

_Это скрапер, то есть сервис позволяющий открывать любые сайты и вытаскивать из них содержимое, удаляя из него лишнее (рекламу из новостных статей, например)._

https://app.scrapingbee.com/account/manage/api_key

**AI DATA EXTRACTION:**

*{"title": "Extract the main article title (not site name, not navigation text, just the article headline)",
"full_article_text": "Extract ONLY the main article content. Exclude: cookie banners, navigation menus, advertisements, social media buttons, footer text, 'Sign in dialog', 'Search dialog', comment sections, and any promotional content. Focus on paragraphs that form the actual article body."}*

**Block Resourses:** ON
**JSON Responce:** ON

**Настройки Credential:**

- **Name:** `api_key` _(если этого поля нет, то не нужно)
_- **Value:** Ваш API ключ

# 4. News Longread Writer

### [1.1] Получаем API HitHub (**Personal access tokens (classic)**)

_ГитХаб я использую в качестве бесплатного текстового редактора, легко работающего с форматированием Markdown. Его можно заменить на Гугл-документы или что-то иное, но мне именно он нравится больше._

[https://github.com/settings/tokens](https://github.com/settings/tokens)

**HEADERS PARAMETRS:
Name:
**Accept
**Value:
**application/vnd.github+json
**Name:
**X-GitHub-Api-Version
**Value:
**2022-11-28
**Настройки Credential:
**Credential Type: GitHub API
**Github Server:
**[https://api.github.com
](https://api.github.com/)**User:
**[ вписать свой ]

### [1.2] Вписать свой ID в “Send Telegram”

### [1.3] Проверяем “Save to Airtable”

**Дата Отчета:
**{{ $json.created_at }}
**Лонгрид_URL:
**{{ $json.gist_url }}
**Использованные_Ссылки:
**{{ $json.topics_covered.join(', ') }}
**Текст_для_Telegram:
**{{ $json.markdown_content.substring(0, 500) + '...' }}
**Telegram_Message_ID:
**{{ String($json.telegram_message_id) }}

# 5. Qualifizer - v0.8

### [1.1] Telegram HTTP typing…

Вставить API ключ своего бота в URL чтобы было _“печатает…”._

**Важно**: **нужен префикс **`**bot**` перед токеном!

Правильный формат:

```text
https://api.telegram.org/bot123456789:GANmgG_qwertyasdfgh-GDS/sendChatAction
```

### [1.2] Check Authorized User (фейсконтроль)

Вписать свой Telegram User ID в поле фильтра. Узнать его можно прямо в N8N во время тестового запуска (найди поле с айдишником).

### [2] Load Reply Context (RPC)

_Это нода для хитровыебанного поиска по базе данных._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301173924-Screenshot_2025-10-22_at_23.42.21.png)

Если проект уже создан, осталось настроить Header Auth и вписать Anon Key.

⚠️ **Как настраивать Credential в ноде “Load Reply Context (RPC)”:

**- **Name: **`**Authorization
**`- **Value: **`**Bearer YOUR_API_KEY

**`***Где искать Anon Key:*** смотри раздел "2. Создаем проект в базе данных Supabase" выше.

# 6. Copywriting Agent

### [1.1] Создаем ключ в SerpAPI:

_Это один из множественных сервисов, позволяющих агентам использовать Google-поиск)._

https://serpapi.com/manage-api-key

### [1.2] Создаем ключ в Jina AI:

_Это сервис, позволяющий агенту открывать любые ссылки._

https://jina.ai/api-dashboard/key-manager

**Resourse:
**Reader
**Operation:
**Read
**URL:
**Defined automatically
**Simplify**: ON

### [2] Telegramify Markdown:

_Это кастомная нода, которая приводит в порядок форматирование, чтобы текст ровно и четко отправлялся телеграм-ботом (N8N очень привередливый)._

**Output Field:
**telegram_text
**Escape Mode:
**Escape

☁️ **(a)** Если у тебя версия [n8n.cloud](http://n8n.cloud), тогда выбери шаблон без _Telegramify,_ там используется форматирование HTML.
**(b)** Если твой N8N установлен на Railway (своем сервере) выбери соответствующий шаблон, и Telegramify будет следить над форматированием MardownV2 (он пизже). Инструкция по разворачиванию N8N на Railway лежит здесь:

На диск залил две версии воркфлоу Копирайтера:

![Screenshot 2025-10-22 at 19.47.38.png](/Users/tom/Documents/Projects/notion/notion/ШАБЛОНЫ N8N [ИИздец]/Команда SMM агентов (v 0 8)/Screenshot_2025-10-22_at_19.47.38.png)

# 7. Image Gen Agent

### [1.1] Создаем ключ в [FAL.AI](http://FAL.AI) и втыкаем Credential

_Это сервис, где можно арендовать модельки для генерации картинок и видео._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301174871-Screenshot_2025-10-22_at_23.46.32.png)

### https://fal.ai/dashboard/keys

**Настройки Credential:**

- **Name:** `Authorization`

- **Value:** `Key YOUR_API_KEY`

### [1.2] Настраиваем flux-pro/v1.1-ultra

- Проверяем URL нужной модельки (лично мне flux нравится, но перенастроить на другую не сложно - нужно поменять ссылку и несколько полей в Body)

- Выбираем размер изображения в Body Parametrs (1:1 / 9:16)

### [2.1] Проверяем “Wait” ноду (10 секунд)

### [2.2] Проверяем настройки “Download Edited Image”

**Retry On Fail:** ON
**Max.Tries:** 3
**Wait Berween Tries:** 5000 ms
**On Error:** (Continue using error output)

# 8. Image Edit Agent

### _[1] Зарегаться на облаке и создать ключ_

_На этот сайт можно загрузить фото и получить ссылку. Это нужно, чтобы модельки для генерации или редактирования изображений легко его распознавали (не во все можно загрузить файл, и они требуют именно ссылку):_

https://api.imgbb.com/

**Body Parameters:
Parameter Type:** Binary File
**Name:** image
**Inpud Data Field Name:** data
**Responce:
Responce Format:** Autodetect
**Настройки Credential:**

- **Name:** `key
`- **Value:** Ваш API ключ

### [2] Проверяем “Nano Banana API”

**BODY JSON:**

{
"prompt": "{{ $json.text }}",
"image_urls": [
"{{ $json.data.url }}"
],
"num_images": 1,
"output_format": "jpeg"
}

### [3.1] Проверяем “Wait” ноду (30 сек)

### [3.2] Проверяем настройки “Download Edited Image”

**Retry On Fail:** ON
**Max.Tries:** 3
**Wait Berween Tries:** 5000 ms
**On Error:** (Continue using error output)

🏄🏽‍♂️ **Поздравляю! Все готово.**

⚡ **Шаблон настроен.**

# ⚠️ ВАЖНЫЕ ДОПОЛНЕНИЯ:

## 1. Мозги для агентов я арендую здесь:

### Open Router

https://openrouter.ai/models

### Open AI API

https://platform.openai.com/settings/organization/api-keys

## 2. У всех агентов ставить Retry On Fail:

Тогда при ошибке (они редко, но случаются) агент попробует повторить запрос. Это включается в настройках ноды. **Пример:**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-smm-team/1767301175669-Screenshot_2025-10-22_at_01.19.51.png)

## 3. Инструкция как развернуть N8N на сервере:

[N8N на Railway (new)](/courses/n8n-mcp/n8n-tpl-railway-new)

## 4. SQL для Supabase (для этого шаблона):

SQL код для создания таблиц показан в видео-инструкции в начале урока.

## 5. Если будут еще дополнения, я напишу здесь.
