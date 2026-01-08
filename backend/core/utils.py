"""
Utility functions for QR code generation and Telegram notifications.
"""
import qrcode
import requests
import logging
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

logger = logging.getLogger(__name__)


def generate_qr_code_image(url):
    """Generate QR code image from URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return ContentFile(buffer.read(), name='qr_code.png')


def send_telegram_message(message, chat_id=None, bot_token=None):
    """Send a message to Telegram chat using Bot API.
    
    Args:
        message: Text message to send
        chat_id: Telegram chat ID (optional, uses settings if not provided)
        bot_token: Telegram bot token (optional, uses settings if not provided)
    
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    from django.conf import settings
    
    bot_token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = chat_id or getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not bot_token or not chat_id:
        logger.warning("Telegram bot token or chat ID not configured")
        return False
    
    try:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(telegram_url, json=payload, timeout=5)
        if response.status_code == 200:
            return True
        else:
            logger.error(f"Telegram API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")
        return False
