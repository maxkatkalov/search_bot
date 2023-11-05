import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from faker import Faker
from dotenv import load_dotenv


load_dotenv()

KEY_WORDS = "Куплю кто кого может сделать решить може зробити вирішити".lower().split()

fake = Faker()


logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher()


@dp.message()
async def echo_with_time(message: Message):
    for word in message.text.split():
        if word.lower() in KEY_WORDS:
            await bot.forward_message(
                chat_id=os.environ.get("ADMIN_CHAT"),
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )


@dp.message(Command("get_chat_id"))
async def get_chat_id(message):
    chat_id = message.chat.id
    await bot.send_message(message.chat.id, f"Chat ID: {chat_id}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
