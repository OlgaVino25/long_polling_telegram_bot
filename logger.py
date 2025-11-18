import logging


class TelegramLogsHandler(logging.Handler):
    """Кастомный обработчик для отправки логов в Telegram"""

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception as e:
            print(f"Не удалось отправить лог в Telegram: {e}")


def setup_logging(bot, admin_chat_id):
    """Настраивает систему логирования"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Обработчик для Telegram
    telegram_handler = TelegramLogsHandler(bot, admin_chat_id)
    telegram_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(levelname)s: %(message)s\n\nTime: %(asctime)s")
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
