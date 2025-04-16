import os
import django
import asyncio
from django.conf import settings
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import StatesGroup, State


# Django sozlamalari
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mafiabot2.settings')
django.setup()

# Django orqali token olish
BOT_TOKEN = settings.BOT_TOKEN

# MemoryStorage ulanishi
storage = MemoryStorage()

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# FSM holatlari
class PlayerState(StatesGroup):
    choosing_action = State()
    voting = State()


# /start komandasi
@dp.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    buttons = [
        [InlineKeyboardButton(text="▶️ O‘yin Boshlash", callback_data="start_game")],
        [InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("👋 Salom! Mafia o‘yiniga xush kelibsiz."
                         "\nQuyidagilardan birini tanlang:", reply_markup=markup)

# start_game callback
@dp.callback_query(F.data == "start_game")
async def game_start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🎲 O‘yin ishtirokchilari yig‘ilmoqda... rollar belgilanadi.")
    await asyncio.sleep(2)

    # 👉 ROLLAR TAQSIMLANADI (bu yerda test uchun oddiy holat)
    await callback.message.answer("👤 Sizning rolingiz: Mafiya\n🕵️ Kechasi siz kimnidir o‘ldirishingiz mumkin.")
    await state.set_state(PlayerState.choosing_action)

    # Simulyatsiya: 10 soniyali kecha bosqichi
    await callback.message.answer("🌙 Kecha boshlandi. Harakat qilish uchun 10 soniya beriladi...")
    await asyncio.sleep(10)

    await callback.message.answer("🌤 Kecha tugadi. Endi kunduzgi ovoz berish boshlanadi.")
    await state.set_state(PlayerState.voting)

    vote_buttons = [
        [InlineKeyboardButton(text="👨 1", callback_data="vote_1")],
        [InlineKeyboardButton(text="👩 2", callback_data="vote_2")],
    ]
    vote_markup = InlineKeyboardMarkup(inline_keyboard=vote_buttons)
    await callback.message.answer("🗳 Kimni osamiz? Ovoz bering:", reply_markup=vote_markup)


# ovoz callbacklari
@dp.callback_query(F.data.startswith("vote_"))
async def handle_vote(callback: CallbackQuery, state: FSMContext):
    voted_id = callback.data.split("_")[1]
    await callback.message.answer(f"✅ Siz {voted_id}-o‘yinchiga ovoz berdingiz.")
    await asyncio.sleep(2)
    await callback.message.answer("🏁 Raund tugadi. Yangi raund boshlanmoqda...")

# yordam
@dp.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🧾 Qoidalar:\n"
        "- Mafiya kechasi kimnidir o‘ldiradi\n"
        "- Komissar tekshiradi\n"
        "- Doktor davolaydi\n"
        "- Tinch aholi o‘ldirilmaslikka harakat qiladi\n"
        "- Kunduz kuni ovoz berib kimnidir osasiz\n\n"
        "Yaxshi o‘yin tilaymiz! 😎"
    )



async def main():
    await dp.start_polling(bot)
