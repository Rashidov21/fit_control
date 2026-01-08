"""
Telegram bot for Fit Control platform.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
from config import BOT_TOKEN, API_BASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()




@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command with QR token."""
    args = message.text.split()
    
    if len(args) > 1:
        # QR code token provided
        token = args[1]
        await handle_qr_registration(message, token)
    else:
        # Regular start
        await message.answer(
            "Salom! Fit Control platformasiga xush kelibsiz.\n\n"
            "QR kod orqali ro'yxatdan o'tish uchun gym adminidan QR kodni oling."
        )


async def handle_qr_registration(message: Message, token: str):
    """Handle QR code-based registration."""
    async with aiohttp.ClientSession() as session:
        try:
            # Verify token and get gym info
            async with session.get(
                f"{API_BASE_URL}/api/auth/verify-qr/{token}/"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('valid'):
                        gym_name = data.get('gym_name', 'Gym')
                        gym_id = data.get('gym_id')
                        
                        # Store gym_id in user data for later use
                        # In production, you'd want to use a proper state management
                        
                        await message.answer(
                            f"QR kod topildi!\n"
                            f"Gym: {gym_name}\n\n"
                            f"Ro'yxatdan o'tish uchun quyidagi ma'lumotlarni yuboring:\n"
                            f"Ism, Familiya, Telefon raqami\n\n"
                            f"Misol: Alisher Karimov +998901234567"
                        )
                    else:
                        await message.answer("QR kod noto'g'ri yoki muddati o'tgan.")
                else:
                    await message.answer("QR kod noto'g'ri yoki muddati o'tgan.")
        except Exception as e:
            logger.error(f"Error verifying QR token: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """Get quick stats for gym admin."""
    # This would require authentication
    # For now, just show a placeholder
    await message.answer(
        "Statistika funksiyasi tez orada qo'shiladi.\n\n"
        "Bu funksiya faqat gym adminlar uchun."
    )


@dp.message(Command("remind"))
async def cmd_remind(message: Message):
    """Send payment reminders to clients."""
    await message.answer(
        "To'lov eslatmalari funksiyasi tez orada qo'shiladi."
    )


@dp.message(Command("promo"))
async def cmd_promo(message: Message):
    """Send promotions to clients."""
    await message.answer(
        "Promo-aksiyalar funksiyasi tez orada qo'shiladi."
    )


async def send_payment_reminder(client_telegram_id: int, client_name: str, amount: float):
    """Send payment reminder to client."""
    try:
        await bot.send_message(
            client_telegram_id,
            f"Salom {client_name}!\n\n"
            f"Oylik to'lov eslatmasi: {amount} so'm\n\n"
            f"Iltimos, to'lovni o'z vaqtida amalga oshiring."
        )
    except Exception as e:
        logger.error(f"Error sending payment reminder: {e}")


async def send_promotion(client_telegram_id: int, promotion_text: str):
    """Send promotion to client."""
    try:
        await bot.send_message(
            client_telegram_id,
            f"🎉 Promo-aksiya!\n\n{promotion_text}"
        )
    except Exception as e:
        logger.error(f"Error sending promotion: {e}")


async def main():
    """Main function to run the bot."""
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
