import os

import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram(chat_id, text):
    """ Отправка сообщения в Телеграм """

    url = f"https://api.telegram.org/bot{os.getenv('API_TOKEN_TELEGRAM')}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }

    requests.get(url, params=params)