from typing import Callable

import aio_pika
import asyncio

from aio_pika.abc import AbstractIncomingMessage


async def run_consumer(
        consumer_name: str,
        queue_name: str,
        handler_function: Callable,
        host: str,
        port: int,
        username: str,
        password: str,
        virtual_host: str = "/"
):
    connection = None
    try:
        connection = await aio_pika.connect_robust(
            host=host,
            port=port,
            login=username,
            password=password,
            virtualhost=virtual_host
        )
        print(f"[{consumer_name}] RabbitMQ connection successful to vhost '{virtual_host}'")

        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(queue_name, durable=True)

        async def message_handler(msg: AbstractIncomingMessage):
            async with msg.process():
                try:
                    message = msg.body.decode('utf-8')
                    print(f"Message Received: {message}")

                    if asyncio.iscoroutinefunction(handler_function):
                        await handler_function(message)
                    else:
                        handler_function(message)

                    print("ACK")

                except Exception as e:
                    print(f"Message Processing Failed: {e}")
                    raise

        await queue.consume(message_handler)
        print(f"[{consumer_name}] Consumer is waiting for messages in queue '{queue_name}'.")
        await asyncio.Future()

    except KeyboardInterrupt:
        print(f"\n[{consumer_name}] Consumer Stopped")
    except Exception as e:
        print(f"[{consumer_name}] Consumer Error: {e}")
    finally:
        if connection and not connection.is_closed:
            await connection.close()
            print(f"[{consumer_name}] RabbitMQ connection closed.")