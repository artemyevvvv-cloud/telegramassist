# Настраиваем вход через Google

**Курс:** Публикация проекта в инет  
**URL:** https://www.aizdec.me/courses/publish/setup-google-auth

---

# 12. Настраиваем вход через Google

Настройка OAuth — это связка двух сервисов: Google и Supabase. Сделаем всё по порядку: сначала все шаги в Google, потом все шаги в Supabase.

## **[ ЧАСТЬ 1: GOOGLE CLOUD ]**

### **Что делаем в Google**

Создаём "пропуск" для твоего приложения. Google должен знать, что твоё приложение существует и имеет право использовать вход через Google.

### **ШАГ 1: Создаём проект**

1. Открой console.cloud.google.com

1. Залогинься под своим Google-аккаунтом

1. Наверху нажми на выпадающий список проектов → **"New Project"**

1. Название: например, "My App Auth"

1. Нажми **"Create"**

### **ШАГ 2: Настраиваем OAuth consent screen**

1. В меню слева: **"APIs & Services"** → **"OAuth consent screen"**

1. User Type: **"External"** → **"Create"**

1. Заполни только обязательные поля:
- **App name** — название приложения
- **User support email** — твой email
- **Developer contact email** — твой email

1. Жми **"Save and Continue"** на каждом шаге до конца

💡 **Интерфейс изменился?**
Google Cloud часто обновляется. Сделай скриншот → отправь Claude → он покажет куда нажать.

### **ШАГ 3: Публикуем приложение**

По умолчанию приложение в режиме "Testing" — это ограничение до 100 пользователей.

1. Перейди в **"OAuth consent screen"**

1. Найди кнопку **"Publish App"**

1. Подтверди публикацию

⚠️ **Важно:**
Без этого шага войти смогут только 100 человек. Для реального проекта — обязательно опубликуй.

### **ШАГ 4: Создаём OAuth Client**

1. В меню: **"APIs & Services"** → **"Credentials"**

1. Нажми **"+ Create Credentials"** → **"OAuth Client ID"**

1. Application type: **"Web application"**

1. Name: любое (например, "Web Client")

**Authorized JavaScript origins:**

```text
https://твой-домен.com
https://my-project.vercel.app
http://localhost:5173
```

Добавь все адреса откуда будут входить пользователи.

**Authorized redirect URIs:**

Оставь пустым — добавим после настройки Supabase.

1. Нажми **"Create"**

### **ШАГ 5: Сохраняем ключи**

Появится окно с двумя значениями:

- **Client ID** — публичный идентификатор

- **Client Secret** — секретный ключ

Скопируй оба в надёжное место (заметки, текстовый файл). Окно можно закрыть — ключи останутся в настройках.

## **[ ЧАСТЬ 2: SUPABASE ]**

### **ШАГ 6: Включаем Google-провайдер**

1. Открой Supabase → твой проект

1. В меню: **"Authentication"** → **"Providers"**

1. Найди **"Google"** → включи переключатель

### **ШАГ 7: Вставляем ключи из Google**

В открывшейся форме:

1. **Client ID** — вставь Client ID из Google

1. **Client Secret** — вставь Client Secret из Google

💡 **Про Client Secret:**
Да, мы вставляем его в Supabase. Это безопасно — Supabase хранит его зашифрованным и использует только на сервере. В браузер пользователя этот ключ никогда не попадает.

### **ШАГ 8: Копируем Callback URL**

Под полями ввода найди **"Callback URL (for OAuth)"**.

Скопируй его. Выглядит так:

```text
https://xxxxx.supabase.co/auth/v1/callback
```

Этот URL нужно добавить в Google.

**Пока НЕ нажимай Save** — сначала добавим URL в Google.

## **[ ЧАСТЬ 3: ФИНАЛЬНАЯ СВЯЗКА ]**

### **ШАГ 9: Добавляем Callback URL в Google**

1. Вернись в Google Cloud → **Credentials**

1. Нажми на свой OAuth Client

1. В разделе **"Authorized redirect URIs"** добавь Callback URL от Supabase

1. Нажми **"Save"**

### **ШАГ 10: Сохраняем в Supabase**

1. Вернись в Supabase → Authentication → Providers → Google

1. Нажми **"Save"**

## **[ ПРОВЕРКА ]**

**Что должно быть готово:**

- [ ] Google Cloud: проект создан

- [ ] Google Cloud: OAuth consent screen настроен

- [ ] Google Cloud: приложение опубликовано (Publish App)

- [ ] Google Cloud: OAuth Client создан с redirect URI от Supabase

- [ ] Supabase: Google-провайдер включён, ключи вставлены

Если всё на месте — переходим к добавлению кнопки входа в приложение.

💭 **От Тома:**
OAuth-настройка выглядит сложной только в первый раз. Много копирования между сервисами, легко что-то пропустить.

Если вход не работает — 90% случаев это опечатка в redirect URI или забытый "Save". Просто пройди по шагам ещё раз.
