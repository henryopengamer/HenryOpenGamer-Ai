import asyncio
import random
import time
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# 🔹 Вставь сюда свой токен от BotFather
TOKEN = "7041656672:AAFTsIXOEY5l4BtDiLNZ0vKd1f1V_KAm3eo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

duel_active = {}
reaction_time = {}

@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    logging.info(f"Команда {message.text} от {message.from_user.id}")
    await message.answer("🤠 Добро пожаловать в дуэльный бот! Введите /duel для начала игры.")

@dp.message(Command("duel"))
async def start_duel(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} начал дуэль.")
    
    if user_id in duel_active:
        await message.answer("🔫 Дуэль уже началась! Ждите сигнал.")
        return
    
    duel_active[user_id] = True
    await message.answer("🤠 Готовьтесь... Ждите сигнал!")
    
    delay = random.uniform(1, 5)
    logging.info(f"Задержка перед 'ОГОНЬ': {delay:.2f} сек.")
    await asyncio.sleep(delay)
    
    reaction_time[user_id] = time.time()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔥 Выстрел!", callback_data="shoot")]])
    
    logging.info(f"Пользователь {user_id} получил команду 'ОГОНЬ!'")
    await message.answer("🔥 ОГОНЬ! ЖМИ!", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "shoot")
async def handle_shoot(call: types.CallbackQuery):
    user_id = call.from_user.id
    logging.info(f"Пользователь {user_id} нажал Выстрел!")
    
    if user_id not in duel_active:
        await call.answer("Вы не в дуэли! Введите /duel")
        return
    
    elapsed_time = time.time() - reaction_time[user_id]
    del duel_active[user_id]
    del reaction_time[user_id]
    
    if elapsed_time < 1.6:
        logging.info(f"Пользователь {user_id} выиграл с реакцией {elapsed_time:.2f} сек.")
        await call.message.answer(f"🎯 Поздравляю, {call.from_user.first_name}! Выстрел за {elapsed_time:.2f} сек. Вы победили! 🤠")
    else:
        logging.info(f"Пользователь {user_id} проиграл, время реакции {elapsed_time:.2f} сек.")
        await call.message.answer(f"💀 Упс... Выстрел за {elapsed_time:.2f} сек. Слишком поздно! Бот победил! 😈")

async def main():
    logging.info("Бот запущен и готов к работе!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
