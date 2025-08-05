import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_telegram_message(text: str):
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Проверка на ошибки HTTP
        logger.info(f"Сообщение отправлено: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {e}")
        return False