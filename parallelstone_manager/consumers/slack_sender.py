import asyncio
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from parallelstone_manager.consumers.consumer import run_consumer
from parallelstone_manager.core.config import settings


QUEUE_NAME = "slack_queue"


def send_message_to_slack(msg: str):
    client = WebClient(token=settings.slack_bot_token)

    try:
        response = client.chat_postMessage(
            channel=settings.slack_channel_id,
            text=msg
        )
    except SlackApiError as e:
        print(e)


async def main():
    await run_consumer(
        consumer_name="Slack",
        queue_name=QUEUE_NAME,
        handler_function=send_message_to_slack,
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
        print("Slack consumer stopped")
    except Exception as e:
        print(f"Slack consumer error: {e}")
        sys.exit(1)
