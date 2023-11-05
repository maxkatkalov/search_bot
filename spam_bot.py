import os
import asyncio
import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from faker import Faker
from dotenv import load_dotenv

import bot

load_dotenv()


fake = Faker()


logging.basicConfig(level=logging.INFO)
spam_bot = Bot(token=os.environ.get("SPAM_BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("generate_fake_messages"))
async def generate_fake_messages_command(message):
    await generate_fake_messages(chat_id=message.chat.id)


async def generate_fake_messages(count: int = 1, chat_id: int = None):
    for _ in range(count):
        await spam_bot.send_message(
            chat_id=chat_id,
            text=fake.text() + f" {random.choice(bot.KEY_WORDS)}"
        )


async def main():
    await dp.start_polling(spam_bot)

if __name__ == "__main__":
    asyncio.run(main())
