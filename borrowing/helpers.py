import requests
from library_service import settings


def send_telegram_message(message: str) -> None:
    """
    Sends a message to the configured Telegram chat using the bot.
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # Optional: Allows for message formatting using HTML tags
    }
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        # Handle the error if needed
        print(f"Failed to send message: {response.text}")
