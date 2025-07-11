import telegram
import asyncio
import sys
from parallelstone_manager.consumers.consumer import BaseConsumer
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


def main():
    """텔레그램 Consumer 메인 함수"""
    print(f"텔레그램 Consumer 시작 중...")
    
    consumer = BaseConsumer(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )
    
    consumer.run_consumer("Telegram", QUEUE_NAME, send_message_tg)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n텔레그램 Consumer 종료")
    except Exception as e:
        print(f"텔레그램 Consumer 오류: {e}")
        sys.exit(1)
