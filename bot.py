import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from faker import Faker
from dotenv import load_dotenv


load_dotenv()

KEY_WORDS = "Куплю кто кого может сделать решить може зробити вирішити".lower().split()

fake = Faker()


logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("get_chat_id"))
async def get_chat_id(message):
    chat_id = message.chat.id
    await bot.send_message(message.chat.id, f"Chat ID: {chat_id}")


@dp.message(Command("get_key_words"))
async def get_key_words(message):
    await bot.send_message(
        message.chat.id,
        f"*Current key words* \({len(KEY_WORDS)}\): {', '.join(KEY_WORDS)}",
        parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.message(Command("add_keyword"))
async def add_keyword(message: Message):
    if message.text:
        command, *new_words_list = message.text.split()
        new_words_list = [new_word.strip().strip(".").lower() for new_word in new_words_list]
        print(new_words_list)

        for new_keyword in new_words_list:
            if new_keyword not in KEY_WORDS:
                KEY_WORDS.append(new_keyword)
                await bot.send_message(
                    message.chat.id,
                    f"Added new keyword: {new_keyword}",
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    f"The keyword '{new_keyword}' is already in the list of keywords",
                )
    else:
        await bot.send_message(
            message.chat.id,
            "Please provide a keyword to add using the /add_keyword command",
        )
        await get_key_words(message)


@dp.message(Command("delete_keyword"))
async def delete_keyword(message: Message):
    if message.text:
        command, *delete_words_list = message.text.split()
        delete_words_list = [delete_word.strip().strip(".").lower() for delete_word in delete_words_list]

        deleted_keywords = []
        for delete_keyword in delete_words_list:
            if delete_keyword in KEY_WORDS:
                KEY_WORDS.remove(delete_keyword)
                deleted_keywords.append(delete_keyword)

        if deleted_keywords:
            await bot.send_message(
                message.chat.id,
                f"Deleted keywords: {', '.join(deleted_keywords)}",
            )
        else:
            await bot.send_message(
                message.chat.id,
                "None of the provided keywords were found in the list of keywords",
            )
        await get_key_words(message)
    else:
        await bot.send_message(
            message.chat.id,
            "Please provide keywords to delete using the /delete_keyword command",
        )


@dp.message()
async def echo_with_time(message: Message):
    for word in message.text.split():
        if word.lower() in KEY_WORDS:
            await bot.forward_message(
                chat_id=os.environ.get("ADMIN_CHAT"),
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
