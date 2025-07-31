import asyncio
import sys

import telegram

from parallelstone_manager.consumers.consumer import run_consumer
from parallelstone_manager.core.config import settings


QUEUE_NAME = "telegram_queue"


async def send_message_tg(msg: str):
    """텔레그램 메시지 전송"""
    try:
        bot = telegram.Bot(token=settings.telegram_bot_token)
        await bot.send_message(chat_id=settings.telegram_chat_id, text=msg)
        print(f"텔레그램 메시지 전송 성공: {msg}")
    except Exception as e:
        print(f"텔레그램 메시지 전송 실패: {e}")
        raise


async def main():
    await run_consumer(
        consumer_name="Telegram",
        queue_name=QUEUE_NAME,
        handler_function=send_message_tg,
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Telegram consumer stopped")
    except Exception as e:
        print(f"Telegram consumer error: {e}")
        sys.exit(1)
