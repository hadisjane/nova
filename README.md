<div align="center">
  <h1>Nova</h1>
  <h3>AI-ассистент для Telegram</h3>

  [![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hadisjane/nova/releases/tag/v1.0.0)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/hadisjane/nova/blob/main/LICENSE)

  [![GitHub](https://img.shields.io/badge/GitHub-00ADD8?style=flat&logo=github&logoColor=white)](https://github.com/hadisjane/nova)
  [![Python Version](https://img.shields.io/badge/Python-3.12+-00ADD8?style=flat&logo=python)](https://www.python.org/)
  [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](https://telegram.org/)
  [![Telethon](https://img.shields.io/badge/Telethon-00ADD8?style=flat&logo=telethon&logoColor=white)](https://docs.telethon.dev/)
  [![Groq](https://img.shields.io/badge/Groq-3863F2?logo=groq&logoColor=white)](https://groq.com)
</div>

---

Nova - это интеллектуальный ассистент для Telegram, созданный на базе Groq AI. Бот умеет вести естественные беседы, запоминать контекст и адаптироваться под стиль общения пользователя.

## 🌟 Основные возможности

- 🧠 Мощная генерация ответов
- 💬 Поддержка длинных диалогов с сохранением контекста
- 🔒 Безопасность и конфиденциальность
- 📊 Подробное логирование всех взаимодействий
- ⚡ Асинхронная работа для высокой отзывчивости
- 🛠️ Гибкая настройка через конфигурационный файл

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.8 или выше
- Учетная запись Telegram
- API ключ от Groq AI

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/hadisjane/nova.git
cd nova
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения в файле `.env`:
```env
# Telegram API credentials
TELEGRAM_API_ID=ваш_api_id
TELEGRAM_API_HASH=ваш_api_hash
TELEGRAM_BOT_TOKEN=ваш_токен_бота если у вас есть бот или пропустите эту строку

# Groq API
GROQ_API_KEY=ваш_groq_api_key

# Настройки
TARGET_USER_IDS=123456789  # ID пользователей через запятую
```

### Получение API ключей

1. **Telegram API**:
   - Перейдите на https://my.telegram.org/
   - Войдите в свой аккаунт
   - Перейдите в раздел "API development tools"
   - Создайте новое приложение и получите `API_ID` и `API_HASH`

2. **Groq API**:
   - Зарегистрируйтесь на https://groq.com/
   - Перейдите в настройки аккаунта
   - Создайте новый API ключ
   - Скопируйте ключ в переменную `GROQ_API_KEY`

## 🏃‍♂️ Запуск

```bash
python3 nova.py
```

## 🏗️ Структура проекта

```
nova/
├── core/                     # Основные модули
│   ├── config.py             # Конфигурация приложения
│   └── memory.py             # Управление памятью и историей
├── api/                      # API интеграции
│   └── nova_api.py           # Работа с Groq API
├── handlers/                 # Обработчики событий
│   └── telegram_handler.py   # Обработчик Telegram
├── utils/                    # Вспомогательные утилиты
│   ├── log_utils.py          # Утилиты логирования
│   └── text_processing.py    # Обработка текста
├── logs/                     # Логи приложения
├── .env                      # Переменные окружения
├── nova.py                   # Основной скрипт
└── requirements.txt          # Зависимости
```

## ⚙️ Настройка

### Переменные окружения

| Переменная | Обязательное | Описание |
|------------|--------------|-----------|
| `TELEGRAM_API_ID` | Да | ID вашего приложения в Telegram |
| `TELEGRAM_API_HASH` | Да | Хеш вашего приложения в Telegram |
| `TELEGRAM_BOT_TOKEN` | Нет | Токен вашего Telegram бота |
| `GROQ_API_KEY` | Да | API ключ от Groq AI |
| `TARGET_USER_IDS` | Да | ID пользователей, которым разрешено общение с ботом (через запятую) |

## 📝 Логирование

Все диалоги сохраняются в директории `logs/` с именами в формате `user_<ID>.log`. Это позволяет анализировать историю общения и улучшать качество ответов.

## 🤝 Вклад в проект

Приветствуются пул-реквесты и предложения по улучшению. Перед внесением изменений:
1. Создайте issue для обсуждения предлагаемых изменений
2. Сделайте форк репозитория
3. Создайте ветку для вашей функции
4. Отправьте pull request с описанием изменений

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## ✨ Благодарности

- [Groq](https://groq.com) за мощный API для генерации текста
- [Telethon](https://docs.telethon.dev/) за удобную работу с Telegram API

## 👨‍💻 Автор

- hadisjane

> 🚀 Проект активно развивается. Присоединяйтесь к разработке!