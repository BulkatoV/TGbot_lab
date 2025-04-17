from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
load_dotenv('token.env')
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список нежелательных слов (цензура)
BLACKLIST = {"дурак", "идиот", "редиска"}  # Можно расширить

# Фильтр: проверяет, содержит ли текст цифры
def has_numbers(message: Message) -> bool:
    return any(char.isdigit() for char in message.text)

# Фильтр: проверяет, содержит ли текст нежелательные слова
def has_bad_words(message: Message) -> bool:
    text_lower = message.text.lower()
    return any(word in text_lower for word in BLACKLIST)

# Команда /start
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        "Привет! Я эхобот с фильтрами. Отправь мне текст или фото.\n"
        "Команды:\n"
        "/caps <текст> - перевести в верхний регистр\n"
        "/reverse <текст> - перевернуть текст\n"
        "/help - помощь"
    )

# Команда /help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        "Фильтры бота:\n"
        "❌ Цензура (запрещенные слова)\n"
        "🔢 Сообщения с цифрами\n"
        "📏 Слишком длинные сообщения (>100 символов)\n\n"
        "Команды:\n"
        "/start - начать\n"
        "/help - помощь\n"
        "/caps <текст> - CAPS LOCK\n"
        "/reverse <текст> - перевернуть текст"
    )

# Обработчик команды /caps
@dp.message(Command(commands=['caps']))
async def caps_command(message: Message):
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not text:
        await message.answer("Пример: /caps привет")
        return
    await message.answer(text.upper())

# Обработчик команды /reverse
@dp.message(Command(commands=['reverse']))
async def reverse_command(message: Message):
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not text:
        await message.answer("Пример: /reverse привет")
        return
    await message.answer(text[::-1])

# Фильтр: сообщения с цифрами
@dp.message(F.text, has_numbers)
async def handle_numbers(message: Message):
    await message.answer("🔢 Я не отвечаю на сообщения с цифрами!")

# Фильтр: нежелательные слова
@dp.message(F.text, has_bad_words)
async def handle_bad_words(message: Message):
    await message.answer("❌ Использование запрещенных слов недопустимо!")

# Фильтр: слишком длинные сообщения
@dp.message(F.text, lambda message: len(message.text) > 100)
async def handle_long_text(message: Message):
    await message.answer("📏 Сообщение слишком длинное (максимум 100 символов).")

# Обработчик фото
@dp.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(f"📸 Получено фото (ID: {message.photo[-1].file_id})")

# Эхо-ответ (только если прошло все фильтры)
@dp.message(F.text)
async def send_echo(message: Message):
    await message.reply(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)