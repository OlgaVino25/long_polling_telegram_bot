import requests
import os
import time
import telebot
from dotenv import load_dotenv


def send_notification(bot, attempt, chat_id):
    """Отправляет уведомление о проверке работы"""
    lesson_title = attempt["lesson_title"]
    lesson_url = attempt.get("lesson_url", "")
    is_negative = attempt["is_negative"]

    if is_negative:
        message = f'❌ Работа "{lesson_title}" проверена!\n\nК сожалению, в работе есть ошибки.\n{lesson_url}'
    else:
        message = f'✅ Работа "{lesson_title}" проверена!\n\nПреподавателю всё понравилось! Можно приступать к следующему уроку.\n{lesson_url}'

    bot.send_message(chat_id=chat_id, text=message)


def main():
    load_dotenv()

    dvmn_api_token = os.getenv("DVMN_API_TOKEN")
    tg_token = os.getenv("DEVMAN_CODE_REVIEW_BOT_TG_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not all([dvmn_api_token, tg_token, chat_id]):
        print("Ошибка: не все необходимые переменные окружения установлены")
        return

    bot = telebot.TeleBot(token=tg_token)

    try:
        chat_info = bot.get_chat(chat_id)
        if chat_info.first_name:
            greeting = f"Привет, {chat_info.first_name}! \nБот запущен и начал отслеживать проверки!"
        elif chat_info.username:
            greeting = f"Привет, @{chat_info.username}! \nБот запущен и начал отслеживать проверки!"
        else:
            greeting = "Привет! \nБот запущен и начал отслеживать проверки!"

        bot.send_message(chat_id=chat_id, text=greeting)

    except Exception as e:
        print(f"Ошибка при отправке приветствия: {e}")

    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {dvmn_api_token}",
    }

    timestamp = None

    while True:
        try:
            params = {}
            if timestamp:
                params["timestamp"] = timestamp

            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            answer = response.json()

            if answer["status"] == "found":
                for attempt in answer["new_attempts"]:
                    send_notification(bot, attempt, chat_id)
                timestamp = answer["last_attempt_timestamp"]

            elif answer["status"] == "timeout":
                timestamp = answer["timestamp_to_request"]

        except requests.exceptions.ReadTimeout:
            print("Таймаут запроса - продолжаем...")
            continue
        except requests.exceptions.ConnectionError:
            print("Проблемы с соединением. Ждем 5 секунд...")
            time.sleep(5)
            continue
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
