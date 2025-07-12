import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from parallelstone_manager.consumers.consumer import BaseConsumer
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


def main():
    consumer = BaseConsumer(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )

    consumer.run_consumer("Slack", QUEUE_NAME, send_message_to_slack)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Slack consumer stopped")
    except Exception as e:
        print("Slack consumer error:", e)
        sys.exit(1)
