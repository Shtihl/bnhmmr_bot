from config import TOKEN, GROUP_ID

import logging
import filters

from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
    await message.delete()


@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эту комманду надо вызывать ответом на сообщение")
        return

    await message.bot.delete_message(GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(
        chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id
    )

    await message.reply_to_message("Зобанен!")


if __name__ == "__main__":
    executor.start_polling(dp)


# https://www.youtube.com/watch?v=I8K3iYcxPl0 зырим и разбираемся дальше
