# Telegram Bot для проверки кода на платформе Devman

Telegram бот для отслеживания статуса проверки работ на платформе Devman. Бот отправляет уведомления в реальном времени о результатах проверки заданий.

## Функциональность

- Отслеживание статуса проверки работ на Devman
- Мгновенные уведомления в Telegram
- Информация о результате проверки (принято/есть ошибки)
- Ссылки на проверенную работу
- Отправка логов об ошибках в Telegram админу
- Автоматический перезапуск при сетевых сбоях
- Запуск как systemd сервис на сервере
- Настройка через переменные окружения

## Технологии

- `Python 3.x`
- `pyTelegramBotAPI` - работа с Telegram Bot API
- `Requests` - HTTP запросы к API Devman
- `python-dotenv` - управление переменными окружения
- `Systemd` - запуск как сервис на сервере
- `Logging` - система логирования с отправкой в Telegram

## Установка

Для запуска у вас уже должен быть установлен `Python 3.x`

1. Клонируйте репозиторий.

2. Установите зависимости командой:

```python
pip install -r requirements.txt
```

## Настройка

1. **Создание Telegram бота**

Создайте бота через [@BotFather](https://t.me/BotFather) и скопируйте токен.

2. **Получение Chat ID**

- Начните диалог с созданным ботом
- Отправьте любое сообщение
- Получите ваш chat_id через @userinfobot или другим способом

3. **Получение Devman API токена**

- Авторизуйтесь на Devman
- Перейдите в раздел API
- Сохраните токен

4. **Настройка конфигурации**

Создать файл `.env` в корне проекта:

```env
DVMN_API_TOKEN=ваш_dvmn_api_здесь
TG_TOKEN=ваш_telegram_bot_токен_здесь
CHAT_ID=ваш_telegram_chat_id_здесь
ADMIN_CHAT_ID=ваш_admin_chat_id_для_логов_здесь
```

## Запуск

```bash
python main.py
```

**После успешного запуска бот отправит приветственное сообщение:**

```text
Привет, Имя! 
Бот запущен и начал отслеживать проверки!
```

**При проверке работы вы получите одно из уведомлений:**

```text
✅ Работа "Название урока" проверена!

Преподавателю всё понравилось! Можно приступать к следующему уроку.
https://dvmn.org/modules/...
```

**В работе есть ошибки:**

```text
❌ Работа "Название урока" проверена!

К сожалению, в работе есть ошибки.
https://dvmn.org/modules/...
```

<img width="268" height="189" alt="Снимок экрана 2025-11-12 062121" src="https://github.com/user-attachments/assets/69069c07-90f7-4f31-91c9-ea0db8997fa4" />

##  Архитектура проекта

```text
devman-telegram-bot/
├── main.py               # Основной файл приложения
├── logger.py             # Система логирования с Telegram-уведомлениями
├── requirements.txt      # Зависимости проекта
├── .gitignore            # Игнорируемые файлы Git
├── .env                  # Переменные окружения (не включен в git)
└── README.md             # Документация
```

## Развертывание на сервере

### Настройка systemd сервиса

Создайте файл `/etc/systemd/system/long-polling-bot.service`:

```ini
[Unit]
Description=Long Polling Telegram Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/long_polling_telegram_bot
EnvironmentFile=/opt/long_polling_telegram_bot/.env
ExecStart=/opt/long_polling_telegram_bot/venv/bin/python3 /opt/long_polling_telegram_bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Активация сервиса:

```bash
sudo systemctl daemon-reload
sudo systemctl enable long-polling-bot
sudo systemctl start long-polling-bot
```

### Мониторинг логов

```bash
sudo journalctl -u long-polling-bot.service -f
```

## Логирование ошибок

Бот настроен на отправку логов об ошибках в отдельный Telegram-чат:
- Ошибки подключения к API Devman
- Проблемы с сетью
- Критические ошибки приложения
- Ошибки отправки сообщений в Telegram

Для настройки необходимо указать `ADMIN_CHAT_ID` в файле `.env`

## Мониторинг и управление

```bash
# Статус сервиса
sudo systemctl status long-polling-bot.service

# Просмотр логов
sudo journalctl -u long-polling-bot.service -f

# Перезапуск сервиса
sudo systemctl restart long-polling-bot.service

# Остановка сервиса
sudo systemctl stop long-polling-bot.service
```


## Особенности реализации

- *Long Polling* - эффективное отслеживание изменений статуса проверок
- *Обработка ошибок* - устойчивость к сетевым сбоям и таймаутам
- *Профессиональное логирование* - информативные сообщения о состоянии системы
- *Systemd сервис* - запуск как демон с автоматическим перезапуском

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
