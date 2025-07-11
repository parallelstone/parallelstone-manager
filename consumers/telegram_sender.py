import telegram
import asyncio
from core import settings

async def send_message_tg(BOT_TOKEN: str, chat_id: str, msg: str):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id = chat_id, text = msg)
