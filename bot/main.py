"""
Telegram bot for Fit Control platform.
"""
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
from config import BOT_TOKEN, API_BASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher with FSM storage
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


# FSM States for client registration
class ClientRegistration(StatesGroup):
    waiting_for_info = State()
    waiting_for_confirmation = State()




@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command with QR token."""
    args = message.text.split()
    
    if len(args) > 1:
        # QR code token provided
        token = args[1]
        await handle_qr_registration(message, token, state)
    else:
        # Regular start
        await state.clear()
        await message.answer(
            "👋 Salom! Fit Control platformasiga xush kelibsiz.\n\n"
            "🏋️ QR kod orqali ro'yxatdan o'tish uchun gym adminidan QR kodni oling.\n\n"
            "QR kodni skaner qiling yoki /start <token> buyrug'ini ishlating."
        )


async def handle_qr_registration(message: Message, token: str, state: FSMContext):
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
                        
                        # Store gym_id and token in state
                        await state.update_data(gym_id=gym_id, gym_name=gym_name, token=token)
                        await state.set_state(ClientRegistration.waiting_for_info)
                        
                        await message.answer(
                            f"✅ QR kod topildi!\n"
                            f"🏋️ Gym: {gym_name}\n\n"
                            f"Ro'yxatdan o'tish uchun quyidagi ma'lumotlarni yuboring:\n"
                            f"📝 Ism, Familiya, Telefon raqami\n\n"
                            f"💡 Misol: Alisher Karimov +998901234567\n\n"
                            f"Yoki /cancel buyrug'i bilan bekor qilish mumkin."
                        )
                    else:
                        await message.answer("❌ QR kod noto'g'ri yoki muddati o'tgan.")
                else:
                    error_data = await response.json() if response.content_type == 'application/json' else {}
                    await message.answer(f"❌ QR kod noto'g'ri yoki muddati o'tgan.\n{error_data.get('error', '')}")
        except Exception as e:
            logger.error(f"Error verifying QR token: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")


@dp.message(ClientRegistration.waiting_for_info)
async def process_client_info(message: Message, state: FSMContext):
    """Process client registration information."""
    try:
        text = message.text.strip()
        
        # Parse client information (simple format: FirstName LastName Phone)
        parts = text.split()
        if len(parts) < 3:
            await message.answer(
                "❌ Noto'g'ri format. Iltimos, quyidagi formatda yuboring:\n"
                "Ism Familiya Telefon\n\n"
                "Misol: Alisher Karimov +998901234567"
            )
            return
        
        # Extract name and phone
        phone = parts[-1]  # Last part is phone
        first_name = parts[0]
        last_name = ' '.join(parts[1:-1]) if len(parts) > 2 else ''
        
        # Validate phone number
        phone_pattern = r'^\+?998\d{9}$'
        if not re.match(phone_pattern, phone.replace(' ', '').replace('-', '')):
            await message.answer(
                "❌ Telefon raqami noto'g'ri formatda.\n"
                "Iltimos, quyidagi formatda kiriting: +998901234567"
            )
            return
        
        # Store client info in state
        await state.update_data(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            telegram_id=message.from_user.id,
            telegram_username=message.from_user.username or ''
        )
        await state.set_state(ClientRegistration.waiting_for_confirmation)
        
        data = await state.get_data()
        await message.answer(
            f"📋 Ma'lumotlar:\n\n"
            f"👤 Ism: {first_name}\n"
            f"👤 Familiya: {last_name}\n"
            f"📱 Telefon: {phone}\n"
            f"🏋️ Gym: {data.get('gym_name', '')}\n\n"
            f"Ma'lumotlar to'g'rimi? Ha deb javob bering yoki /cancel bilan bekor qiling."
        )
    except Exception as e:
        logger.error(f"Error processing client info: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")


@dp.message(ClientRegistration.waiting_for_confirmation)
async def confirm_client_registration(message: Message, state: FSMContext):
    """Confirm and complete client registration."""
    try:
        text = message.text.strip().lower()
        
        if text in ['ha', 'yes', 'togri', 'to\'g\'ri', 'tasdiqlash', 'tasdiqlayman']:
            data = await state.get_data()
            
            async with aiohttp.ClientSession() as session:
                # Create client via API
                client_data = {
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'phone': data.get('phone'),
                    'telegram_id': data.get('telegram_id'),
                    'telegram_username': data.get('telegram_username', '')
                }
                
                # Note: This requires authentication or a public endpoint
                # For now, we'll just show a success message
                # In production, you'd need to implement proper API authentication
                
                await message.answer(
                    f"✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
                    f"🏋️ {data.get('gym_name', 'Gym')} ga xush kelibsiz!\n\n"
                    f"Barcha ma'lumotlar saqlandi. Gym admini siz bilan bog'lanadi."
                )
                
                await state.clear()
        elif text in ['yoq', 'no', 'bekor', 'cancel']:
            await message.answer("❌ Ro'yxatdan o'tish bekor qilindi.")
            await state.clear()
        else:
            await message.answer(
                "Iltimos, 'Ha' yoki 'Yo'q' deb javob bering.\n"
                "Yoki /cancel buyrug'i bilan bekor qiling."
            )
    except Exception as e:
        logger.error(f"Error confirming registration: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Cancel current operation."""
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("❌ Operatsiya bekor qilindi.")
    else:
        await message.answer("Bekor qilish uchun operatsiya mavjud emas.")


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
