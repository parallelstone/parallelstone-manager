import telegram
import asyncio
from consumer import BaseConsumer
from core import settings


QUEUE_NAME = "telegram_queue"


async def send_message_tg(msg: str):
    bot = telegram.Bot(token=settings.telegram_bot_token)
    await bot.send_message(chat_id=settings.telegram_chat_id, text=msg)



if __name__ == '__main__':
    consumer = BaseConsumer(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )
    if consumer.connect():
        print(f"{QUEUE_NAME} 큐에서 메시지 대기 중...")
        consumer.consume_queue(QUEUE_NAME, send_message_tg)
    else:
        print("연결 실패로 인해 Consumer를 시작할 수 없습니다.")
