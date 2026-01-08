"""
Configuration for Telegram bot.
"""
from decouple import config

# Telegram Bot
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
BOT_USERNAME = config('TELEGRAM_BOT_USERNAME', default='')

# Django API
API_BASE_URL = config('API_BASE_URL', default='http://localhost:8000')
API_USERNAME = config('API_USERNAME', default='')
API_PASSWORD = config('API_PASSWORD', default='')
