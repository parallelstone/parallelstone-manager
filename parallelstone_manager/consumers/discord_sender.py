import asyncio
import sys
import aiohttp

from parallelstone_manager.consumers.consumer import run_consumer
from parallelstone_manager.core.config import settings


QUEUE_NAME = "discord_queue"


async def send_message_discord(message: str):
    """Discord HTTP API로 메시지 전송"""
    channel_id = settings.discord_channel_id
    bot_token = settings.discord_bot_token
    
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    print(f"Discord 메시지 전송 성공: {message}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"Discord 메시지 전송 실패: {response.status} - {error_text}")
                    return False
    except Exception as e:
        print(f"Discord 메시지 전송 오류: {e}")
        return False


async def main():
    await run_consumer(
        consumer_name="Discord",
        queue_name=QUEUE_NAME,
        handler_function=send_message_discord,
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDiscord consumer stopped")
    except Exception as e:
        print(f"Discord consumer error: {e}")
        sys.exit(1)
