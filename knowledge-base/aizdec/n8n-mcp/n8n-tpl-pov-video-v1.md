# Фабрика POV видео (v1.1)

**Курс:** N8N + Claude Code  
**URL:** https://www.aizdec.me/courses/n8n-mcp/n8n-tpl-pov-video-v1

---

💽 [**ССЫЛКА НА ШАБЛОН**](https://drive.google.com/file/d/1NODIzyYItcI5o_Hy-ennAahqIqdft9ee/view?usp=sharing)

📖 [**ССЫЛКА НА ТАБЛИЦУ**](https://docs.google.com/spreadsheets/d/1SP_lUVvMlBY2mrN9zCjGgbDUCDioC3ZkSTS7FwZDk5s/edit?usp=sharing)

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301139058-______________2025-04-05___05.11.48.png)

### 🔍 Что делает:

Этот шаблон создает вирусные исторические POV видео (от первого лица), которые собирают миллионы просмотров в TikTok, Inst и YouTube Shorts. Он берет каждую идею из Google Таблицы –> генерирует последовательный сюжет _"дня из жизни"_ -> а затем для каждой сцены выполняет конвейер задач: _создание изображений, анимация, наложение звуков, монтаж._

### 💻 Сервисы и интеграции:

- **N8N** — конструктор

- **Google Sheets** — для хранения идей и сохранения финальных ссылок

- **Google Drive** — для временного хранения аудиофайлов (OAuth2)

- [**OpenAI**](https://platform.openai.com/api-keys) — для сценариев и промптов

- [**PiAPI.ai**](https://piapi.ai/workspace) — для изображений Flux, а для видео Kling

- [**ElevenLabs**](https://elevenlabs.io/) — для генерации звуковых эффектов

- [**Creatomate**](https://creatomate.com/) — для финального видео-монтажа

- **YouTube** — Для публикации видео

### ⚙️ Установка и настройка

1. Подключаем сервисы Google

1. Создаём таблицу

1. Регаемся на [PiAPI.AI](http://piapi.ai/)

1. Соединяемся с ElevenLabsё

1. Настраиваем Creatomate

1. Финалим таблицу

1. Дополнительные детали

## 1️⃣ Подключаем сервисы Google

- **Таблицы (Sheets)**:

Тут всё слишком просто. Можно даже не комментировать.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301139664-______________2025-04-04___22.50.58.png)

- **Диск (Drive)**:

Данный урок подразумевает, что тобой уже изучены все предыдущие лекции. Поэтому супер-базовые нюансы я разбирать не буду. **Этого должно быть достаточно:**

Скопируй _OAuth Redirect URL_ –> и зайди на сайт _Google_ _Cloude Console._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301140037-______________2025-04-04___23.21.47.png)

Там найди _Google Drive API_ –> жми **Enable / Manage.**

И перейди в _Credentials_ –> чтобы создать новое подключение.

Нам нужно OAuth 2.0. Тыкни на **+ Create credentials**.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301140594-______________2025-04-04___23.23.50.png)

Здёсь всё стандартно.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301141022-______________2025-04-04___23.28.06.png)

А в поле ниже воткни **URL**, скопированный в N8N.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301141427-______________2025-04-04___23.29.17.png)

После нажатия **Create** –> увидишь это:

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301141869-______________2025-04-04___23.32.22.png)

Копируем _Client ID_ и _Сlient Secret_.

И вставляем их в Credential N8N.

После чего тыкаем **Sign in with Google** и ставим галочки.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301142215-______________2025-04-04___23.35.42.png)

**Готово :)**

Теперь можно перейти в свой Google Drive и создать отдельную папку для аудиозаписей. После того как сделаешь это, вернись в N8N и выбери её название в узле _Upload Mp3._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301142536-______________2025-04-05___03.08.24.png)

### ✅ С Гуглом почти разобрались.

## 2️⃣ Создаём таблицу

Она нужна для прописывания идей _(первый раз для теста мы заполним их вручную, а потом можно подключить на эту задачу отдельного агента)_ + сохранения итоговых результатов. **Перейди в мою **[таблицу](https://docs.google.com/spreadsheets/d/1SP_lUVvMlBY2mrN9zCjGgbDUCDioC3ZkSTS7FwZDk5s/edit?usp=sharing)** и жми –>** **Создать копию.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301142862-______________2025-04-04___23.46.34.png)

_Внутри уже есть первый пример для теста.Но ты можешь скопировать название нужных столбцов, и попросить ChatGPT сгенерировать тебе свою таблицу по нужным идеям / нишам._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301143230-______________2025-04-04___23.51.36.png)

**Описание таблицы:**

- **idea** - содержит описание POV-сцены.

- **caption** - описание деталей (если нужно).

- **enviroment_prompt** - задаёт год, место, визуальные детали.

- **production** - статус готовности, чтобы агент помечал видео.

- **publishing** - статус публикации, чтобы проверять залит ли видос.

- **final_output** - здесь будет ссылка на итоговый результат.

### ✅ Идём дальше.

## 3️⃣ Регаемся на [PiAPI.AI](http://piapi.ai/)

Что тут есть – можно увидеть на скрине. Сервис даёт бесплатные токены для теста. Когда потребуется оплатить, это можно будет сделать с помощью карты или крипты.

Я за секунду вошел через GitHub.

А далее –> перешел в **Settings** –> **API Keys.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301143774-______________2025-04-05___00.09.55.png)

Придумай название и сделай новый ключ.

Скопируй его и пошли настраивать узлы в N8N.

- **Создание изображений:**_Text to image + Get Image_

Начнём отсюда. На данном шаге мы отправляем сгенерированные промты в Kling чтобы он сгенерировал для нас пикчи, которые позже будут анимированы.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301144293-______________2025-04-05___00.12.12.png)

Листаем немного вниз и ищем поле для ключа.

Втыкай его в –> _Value_.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301144604-______________2025-04-05___00.13.17.png)

Здесь повторяем те же действия. Данный шаг получает готовые изображения после паузы (у меня стоит 2 минуты, при желании можно увеличить).

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301144911-______________2025-04-05___00.17.35.png)

Ну и готово, получается.

С изображениями разобрались.

- **Генерация видео:
**_Image to video + Get Video_

На этом шаге мы отправляем запрос в Kling.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301145243-______________2025-04-05___00.28.11.png)

Затем пауза. Немного больше, чем на предыдущем шаге, потому что видео генерятся дольше изображений (я оставил 10 мин).

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301145549-______________2025-04-05___00.31.52.png)

Ну и здесь API ключ не забываем.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301145874-______________2025-04-05___00.34.14.png)

### ✅ Самое сложное сделали!

## 4️⃣ Соединяемся с ElevenLabs

Этот прекрасный сервис умеет не только озвучивать агентов, но и создавать звуки для наших POV видео. Поэтому мы быстро регаемся, если еще не сделали этого –> получаем бесплатные токены –> и идём в **API Keys.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301146229-______________2025-04-05___00.41.48.png)

Тут придумываем название нового ключа и копируем его.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301146550-______________2025-04-05___00.44.24.png)

Возвращаемся в N8N и втыкаем ключ в узел –> _Text to sound._

В поле _Value_.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301147025-______________2025-04-05___00.46.30.png)

### ✅ Для звуков всё готово :)

## 5️⃣ Настраиваем Creatomate

Это сервис для автоматизированных склеек. Он не единственный и даже не самый удобный. Кроме того, он требует оплаты тарифа для генерации в хорошем качестве (для теста хватит бесплатной версии).

В следующем уроке я покажу альтернативу, но с _Creatomate_ все равно нужно познакомиться, потому что опытному специалисту важно иметь широкий арсенал. А также понимать плюсы и минусы каждого отдельного инструмента.

После создания проекта, жмем на три точки **...** в левом верхнем углу.

И заходим в **Project Settings.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301147357-______________2025-04-05___01.23.52.png)

Здесь нас интересует _API Key._

Копируем его.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301147748-______________2025-04-05___01.21.31.png)

Возвращаемся в N8N –> открываем узел _Render Video.
_**И вставляем ключ вот так:** _Bearer ключ_  (между ними пробел).

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301148075-______________2025-04-05___01.15.43.png)

Узел подключили (ﾉ◕ヮ◕)ﾉ*:

Теперь возвращаемся в Creatomate.

Нам нужно создать шаблон для будущих видео.

**Tempates –> + New**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301148401-______________2025-04-05___05.25.15.png)

Далее жми –> **Start from scratch**

И выбери формат _9:16 Vertical_ (потому что щас всё делаем под него).

Затем –> **Create Template.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301148769-______________2025-04-05___01.32.35.png)

Теперь нам нужна кнопка **{..}** в верхнем меню.

Этот раздел также открывается через F12 на клавиатуре.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301149163-______________2025-04-05___01.34.25.png)

## Вставь туда этот код:

_Он расчитан на 5 отрезков в видео. Тебе этого может быть мало, поэтому в конце я оставлю код для 12 фрагментов. Изучив оба, ты поймешь как настраивать этот дело под свои задачи. Ну или ChatGPT тебе обьснит :)_

```text
{
  "output_format": "mp4",
  "width": 1080,
  "height": 1920,
  "elements": [
{
  "id": "476fbf11-185a-4842-bb54-8fbe5ede8f45",
  "name": "Audio-1",
  "type": "audio",
  "track": 1,
  "time": 0,
  "source": "b61010d4-adcf-4d93-8546-934e5a4b448a",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "50d079ac-a1cb-4169-a720-9148d05845f1",
  "name": "Audio-2",
  "type": "audio",
  "track": 1,
  "time": 5,
  "source": "0109fa02-239b-4baa-ab5c-1e0445276cb7",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "78edca64-24af-47f3-9496-a3d03afa4038",
  "name": "Audio-3",
  "type": "audio",
  "track": 1,
  "time": 10,
  "source": "8e323742-21f3-437d-a163-01a05154b216",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "97b1258a-a398-4824-afaf-c87ae87048f4",
  "name": "Audio-4",
  "type": "audio",
  "track": 1,
  "time": 15,
  "source": "458c2f63-6abf-4058-8f99-3d11efdf3ce5",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "2a6b8dcf-2b2d-4739-9389-2fd4edee02d1",
  "name": "Audio-5",
  "type": "audio",
  "track": 1,
  "time": 20,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "db018ee8-4530-4cc4-9fb4-4cc034a7985f",
  "name": "Video-1",
  "type": "video",
  "track": 2,
  "time": 0,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "07c6aa87-c882-4307-a49d-0fad9507fc80",
  "name": "Video-2",
  "type": "video",
  "track": 2,
  "time": 5,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "f4526c6e-fe95-4bb9-99d3-284faaea3832",
  "name": "Video-3",
  "type": "video",
  "track": 2,
  "time": 10,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "5153165c-8630-4488-a1e0-5afdfbec6225",
  "name": "Video-4",
  "type": "video",
  "track": 2,
  "time": 15,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "28c2600a-f255-4d1c-aab7-c02801ae5d4f",
  "name": "Video-5",
  "type": "video",
  "track": 2,
  "time": 20,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-1",
  "type": "text",
  "track": 3,
  "time": 0,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-2",
  "type": "text",
  "track": 3,
  "time": 5,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
 {
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-3",
  "type": "text",
  "track": 3,
  "time": 10,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-4",
  "type": "text",
  "track": 3,
  "time": 15,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-5",
  "type": "text",
  "track": 3,
  "time": 20,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
}
  ]
}

```

**Получится так:**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301149685-______________2025-04-05___01.41.40.png)

Теперь жми **Use Template** в правом верхнем углу.

И выбери в меню **API Integration.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301150382-______________2025-04-05___01.45.46.png)

Тут нам нужно скопировать _"template_id"._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301150910-______________2025-04-05___01.47.25.png)

Возвращаемся в N8N –> в узел _Render Video._

И вставляем скопированный ID в _Body_ _(я выделил на скрине)._

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301151442-______________2025-04-05___05.28.42.png)

⚠️ **ВАЖНО:** _если будешь увеличивать количество отрезков, то нужно обновлять не только код в Cratomate, но и в узле Render Video. Ниже я дам код для 12 отрезков._

### ✅ С "монтажом" разобрались.

### 6️⃣ Финалим таблицу

После того, как все сгенерируется, агент должен обновить таблицу. Для этого открываем узел _Update google sheet_. И проверяем чтобы тут у нас.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301151782-______________2025-04-05___02.27.01.png)

- _id (using to match)_ –> втыкается АйДи из таблицы (по сути это просто цифра, которой помечен номер идеи). Это нужно чтобы обновить поля.

- _production_ –> проставляется Done

- publishing –> проставляется Ready

### Я сам щас прогнал шаблон

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301152172-______________2025-04-05___05.32.16.png)

### ✅ и вижу, что мы всё настроили!

**Таблица обновилась и я уже поставил оценку полученному видео.**

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301152706-______________2025-04-05___05.34.11.png)

## 7️⃣ Дополнительные детали

**Быстро о том, что не затронул выше:**

### А. **Генерация идей**

Данный узел переделывает идеи из нашей таблицы в сцены.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301153070-______________2025-04-05___02.56.44.png)

Промт этого агента объясняет ему как разбивать идею на отрезки. Не бойся экспериментировать. Под каждый проект лучше настраивать отдельный процесс, учитывающий особенности ниши (например, исторический формат).

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301153547-______________2025-04-05___03.00.40.png)

_Item List Otput Parser_ отвечает за количество отрезков в будущих видео. Если поставить 5 –> значит идея превратится в последовательный сценарий из 5 частей.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301154150-______________2025-04-05___02.57.52.png)

⚠️ **ВАЖНО:** чтобы у тебя при тестировании не сожрались все токены за несколько минут, в шаблоне по умолчанию стоит **2** _Number Of Items._

### Б. Генерация звуков

Здесь название отрезков передается в _11Labs_ для озвучки.

Описание для инструмента выглядит так:

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301154458-______________2025-04-05___05.37.54.png)

Это HTTP запрос к сервису _(грубо говоря, мы отправляем в 11Labs письмо со словами: "вот такой вот звук сделай мне и потом получаем ответ".)_ В N8N не всегда есть нужные нам ноды/узлы, а таким образом можно позволить себе намнооого больше.

MCP, конечно, дико упрощает внешние подключения, и подобные интеграции. Но это тема отдельного урока. Начинаем с базы.

### В. Публикация результата

Я пока отключил этот узел в шаблоне, потому что дальше у нас будет целый блок о подключении всех возможных социальных сетей. Ты сможешь легко его врубить обратно. Разобраться не сложно.

![image](https://ajvmyjuqfdjrljmodbdb.supabase.co/storage/v1/object/public/lesson-media/lessons/n8n-tpl-pov-video-v1/1767301154817-______________2025-04-05___03.31.22.png)

## ▶️ Можно тестировать

### Инструкция для тестового запуска:

1. **Подготовь данные в таблице
**Убедись, что в Google Таблице есть строка с полями `idea`, `enviroment_prompt`, `production = for production`.

1. **Запусти workflow вручную
**Нажми "Test workflow" в N8N.

1. **Проверь узел Titles и идеи (сценарист)
**Убедись, что он возвращает короткие сцены в `text`.

1. **Проверь узел OpenAI (промтовик)
**На выходе должен быть один англоязычный prompt в `message.content`, соответствующий сцене.

1. **Проверь Text to image
**Убедись, что используется правильный prompt и что `image_url` получен после Get Image. Работоспособность модельки можно также проверить на сайте _PiAPI_ в разделе _Task History._

1. **Проверь Image to video
**Проверь, что `prompt` и `image_url` передаются правильно. Убедись, что видео сгенерировано. При наличии ошибок дополнительно проверь _Task History._

1. **Проверь Text to sound
**Убедись, что звук сгенерирован по соответствующему promptу и что получен mp3-файл.

1. **Проверь Merge1 и Code1
**Убедись, что все массивы (text, video, sound) одной длины и в правильном порядке. Если они группируются вместе без ошибок – значит все четко.

1. **Проверь Render Video
**Убедись, что `scene_titles`, `video_urls`, `sound_urls` подставляются правильно.

1. **Проверь результат
**Открой ссылку `final_output` из таблицы и убедись, что в видео:
- сцена соответствует описанию
- есть звук
- есть надпись

**УРА!!!!**

Ты только что запустил автоматизацию для создания (исторических POV) видео от канала ИИздец. Она берёт идеи из таблицы, превращает их в сценарии, создает по ним изображения, анимирует их, добавляет звуки и склеивает вместе.

## 🚨 Частые вопросы

**❓ Что делать при ошибках?**

➡️ Использовать ChatGPT:

- В подписке на ChatGPT за $20 и $200 есть модельки, которые хорошо справляются с подобными задачами _(на апрель 2025 это 4о)._

- Отправь ей JSON файл. Затем четко сформулируй свой вопрос и прикрепи скриншот / скопируй описание ошибки _(N8N всегда справа присылает output с результатом и если че-т не работает, там почти всегда написано почему)._

- Чем больше вводных, тем лучше. Но не забывай про ограничения контекста моделки, с которой ты общаешься. Спустя какое-то время после начала диалога, общение будет становиться менее эффективным. Тогда можно будет начать новый диалог, заново объяснить происходящее, сформулировать новые вопросы и продолжить.

**❓ Как изменить стиль видео?**

➡️ Главный инструмент – это промты, а именно:

- Идеи в Google Таблице и описание деталей.

- Системный промт агента сценариста.

- Инструкция для агента промтовика.

➡️ На стиль также влияют модельки, выбранные для генерации. Одни умеют лучше в анимационный стиль, другие в реализм. В интернете масса обзоров все существующих нейросетей, поэтому можешь выбирать что по кайфу. Как подключать к чему угодно через HTTP запросы я показал.

**❓ Можно ли изменить количество сцен?**

➡️ Да, для этого нужно:

- В узле `Item List Output Parser` измени цифру `Number Of Items`.

- В узле `Code (List Elements)` измени код JavaScript, чтобы он обрабатывал нужное количество элементов (щас прописано под 5).

- Адаптируй свой шаблон в _Creatomate_ под новое количество сцен.

### Код для узла Render Video (12 узлов):

```text
{
  "template_id": "5aafffa3-6adc-4a2f-90dc-c91a80d2136a",
  "modifications": {
"Audio-1.source": "{{ $json.sound_urls[0] }}",
"Audio-2.source": "{{ $json.sound_urls[1] }}",
"Audio-3.source": "{{ $json.sound_urls[2] }}",
"Audio-4.source": "{{ $json.sound_urls[3] }}",
"Audio-5.source": "{{ $json.sound_urls[4] }}",
"Audio-6.source": "{{ $json.sound_urls[5] }}",
"Audio-7.source": "{{ $json.sound_urls[6] }}",
"Audio-8.source": "{{ $json.sound_urls[7] }}",
"Audio-9.source": "{{ $json.sound_urls[8] }}",
"Audio-10.source": "{{ $json.sound_urls[9] }}",
"Audio-11.source": "{{ $json.sound_urls[10] }}",
"Audio-12.source": "{{ $json.sound_urls[11] }}",

"Video-1.source": "{{ $json.video_urls[0] }}",
"Video-2.source": "{{ $json.video_urls[1] }}",
"Video-3.source": "{{ $json.video_urls[2] }}",
"Video-4.source": "{{ $json.video_urls[3] }}",
"Video-5.source": "{{ $json.video_urls[4] }}",
"Video-6.source": "{{ $json.video_urls[5] }}",
"Video-7.source": "{{ $json.video_urls[6] }}",
"Video-8.source": "{{ $json.video_urls[7] }}",
"Video-9.source": "{{ $json.video_urls[8] }}",
"Video-10.source": "{{ $json.video_urls[9] }}",
"Video-11.source": "{{ $json.video_urls[10] }}",
"Video-12.source": "{{ $json.video_urls[11] }}",

"Text-1.text": "{{ $json.scene_titles[0] }}",
"Text-2.text": "{{ $json.scene_titles[1] }}",
"Text-3.text": "{{ $json.scene_titles[2] }}",
"Text-4.text": "{{ $json.scene_titles[3] }}",
"Text-5.text": "{{ $json.scene_titles[4] }}",
"Text-6.text": "{{ $json.scene_titles[5] }}",
"Text-7.text": "{{ $json.scene_titles[6] }}",
"Text-8.text": "{{ $json.scene_titles[7] }}",
"Text-9.text": "{{ $json.scene_titles[8] }}",
"Text-10.text": "{{ $json.scene_titles[9] }}",
"Text-11.text": "{{ $json.scene_titles[10] }}",
"Text-12.text": "{{ $json.scene_titles[11] }}"
  }
}

```

### Код для Creatomate Template (12 узлов):

```text
{
  "output_format": "mp4",
  "width": 1080,
  "height": 1920,
  "elements": [
{
  "id": "476fbf11-185a-4842-bb54-8fbe5ede8f45",
  "name": "Audio-1",
  "type": "audio",
  "track": 1,
  "time": 0,
  "source": "b61010d4-adcf-4d93-8546-934e5a4b448a",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "50d079ac-a1cb-4169-a720-9148d05845f1",
  "name": "Audio-2",
  "type": "audio",
  "track": 1,
  "time": 5,
  "source": "0109fa02-239b-4baa-ab5c-1e0445276cb7",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "78edca64-24af-47f3-9496-a3d03afa4038",
  "name": "Audio-3",
  "type": "audio",
  "track": 1,
  "time": 10,
  "source": "8e323742-21f3-437d-a163-01a05154b216",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "97b1258a-a398-4824-afaf-c87ae87048f4",
  "name": "Audio-4",
  "type": "audio",
  "track": 1,
  "time": 15,
  "source": "458c2f63-6abf-4058-8f99-3d11efdf3ce5",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "2a6b8dcf-2b2d-4739-9389-2fd4edee02d1",
  "name": "Audio-5",
  "type": "audio",
  "track": 1,
  "time": 20,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "name": "Audio-6",
  "type": "audio",
  "track": 1,
  "time": 25,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "p7q8r9s0-t1u2-v3w4-x5y6-z7a8b9c0d1e2",
  "name": "Audio-7",
  "type": "audio",
  "track": 1,
  "time": 30,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8",
  "name": "Audio-8",
  "type": "audio",
  "track": 1,
  "time": 35,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "v9w0x1y2-z3a4-b5c6-d7e8-f9g0h1i2j3k4",
  "name": "Audio-9",
  "type": "audio",
  "track": 1,
  "time": 40,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "l5m6n7o8-p9q0-r1s2-t3u4-v5w6x7y8z9a0",
  "name": "Audio-10",
  "type": "audio",
  "track": 1,
  "time": 45,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "b1c2d3e4-f5g6-h7i8-j9k0-l1m2n3o4p5q6",
  "name": "Audio-11",
  "type": "audio",
  "track": 1,
  "time": 50,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "r7s8t9u0-v1w2-x3y4-z5a6-b7c8d9e0f1g2",
  "name": "Audio-12",
  "type": "audio",
  "track": 1,
  "time": 55,
  "source": "38eeb087-d6a5-41ae-b3d8-67ae8345ab85",
  "trim_duration": 5,
  "dynamic": true
},
{
  "id": "db018ee8-4530-4cc4-9fb4-4cc034a7985f",
  "name": "Video-1",
  "type": "video",
  "track": 2,
  "time": 0,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "07c6aa87-c882-4307-a49d-0fad9507fc80",
  "name": "Video-2",
  "type": "video",
  "track": 2,
  "time": 5,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "f4526c6e-fe95-4bb9-99d3-284faaea3832",
  "name": "Video-3",
  "type": "video",
  "track": 2,
  "time": 10,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "5153165c-8630-4488-a1e0-5afdfbec6225",
  "name": "Video-4",
  "type": "video",
  "track": 2,
  "time": 15,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "28c2600a-f255-4d1c-aab7-c02801ae5d4f",
  "name": "Video-5",
  "type": "video",
  "track": 2,
  "time": 20,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "h3i4j5k6-l7m8-n9o0-p1q2-r3s4t5u6v7w8",
  "name": "Video-6",
  "type": "video",
  "track": 2,
  "time": 25,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "x9y0z1a2-b3c4-d5e6-f7g8-h9i0j1k2l3m4",
  "name": "Video-7",
  "type": "video",
  "track": 2,
  "time": 30,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "n5o6p7q8-r9s0-t1u2-v3w4-x5y6z7a8b9c0",
  "name": "Video-8",
  "type": "video",
  "track": 2,
  "time": 35,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6",
  "name": "Video-9",
  "type": "video",
  "track": 2,
  "time": 40,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "t7u8v9w0-x1y2-z3a4-b5c6-d7e8f9g0h1i2",
  "name": "Video-10",
  "type": "video",
  "track": 2,
  "time": 45,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "j3k4l5m6-n7o8-p9q0-r1s2-t3u4v5w6x7y8",
  "name": "Video-11",
  "type": "video",
  "track": 2,
  "time": 50,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "z9a0b1c2-d3e4-f5g6-h7i8-j9k0l1m2n3o4",
  "name": "Video-12",
  "type": "video",
  "track": 2,
  "time": 55,
  "duration": 5,
  "source": "4d90054a-61a7-4d8e-8fcf-a0418e473cca",
  "clip": true,
  "dynamic": true
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bd",
  "name": "Text-1",
  "type": "text",
  "track": 3,
  "time": 0,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204be",
  "name": "Text-2",
  "type": "text",
  "track": 3,
  "time": 5,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204bf",
  "name": "Text-3",
  "type": "text",
  "track": 3,
  "time": 10,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c0",
  "name": "Text-4",
  "type": "text",
  "track": 3,
  "time": 15,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c1",
  "name": "Text-5",
  "type": "text",
  "track": 3,
  "time": 20,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c2",
  "name": "Text-6",
  "type": "text",
  "track": 3,
  "time": 25,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c3",
  "name": "Text-7",
  "type": "text",
  "track": 3,
  "time": 30,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c4",
  "name": "Text-8",
  "type": "text",
  "track": 3,
  "time": 35,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c5",
  "name": "Text-9",
  "type": "text",
  "track": 3,
  "time": 40,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c6",
  "name": "Text-10",
  "type": "text",
  "track": 3,
  "time": 45,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c7",
  "name": "Text-11",
  "type": "text",
  "track": 3,
  "time": 50,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
},
{
  "id": "04bb636f-0b96-4a0f-9125-d662eb7204c8",
  "name": "Text-12",
  "type": "text",
  "track": 3,
  "time": 55,
  "duration": 5,
  "x": "2.7527%",
  "y": "17.1734%",
  "width": "94.4945%",
  "height": "7.8841%",
  "x_anchor": "0%",
  "y_anchor": "0%",
  "x_alignment": "50%",
  "y_alignment": "50%",
  "text": "Lifting a heavy tapestry to reveal sunlight streaming in",
  "font_family": "Oswald",
  "font_weight": "700",
  "font_size": "7 vmin",
  "background_color": "#1d1d1d",
  "fill_color": "#ffffff",
  "animations": [
    {
      "time": 0,
      "duration": 1,
      "easing": "quadratic-out",
      "type": "text-appear",
      "split": "letter"
    },
    {
      "time": "end",
      "duration": 1,
      "easing": "quadratic-out",
      "reversed": true,
      "type": "text-appear",
      "split": "letter"
    }
  ]
}
  ]
}

```
