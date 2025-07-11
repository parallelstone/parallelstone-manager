import pika
import asyncio

from core import settings

class BaseConsumer:
    def __init__(self):
        self.host = settings.rabbitmq_host
        self.port = settings.rabbitmq_port
        self.user = settings.rabbitmq_username
        self.password = settings.rabbitmq_password
        self.virtual_host = settings.rabbitmq_virtual_host
        self.connection = None
        self.channel = None


    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=pika.PlainCredentials(self.user, self.password),
                    virtual_host=self.virtual_host
                )
            )
            self.channel = self.connection.channel()
            return True
        except Exception as e:
            print(f"Consumer connection error: {e}")
            return False


    def disconnect(self):
        self.connection.close()

    def consume_queue(self, queue_name: str, function):
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)

            # 메시지 처리 wrapper 함수
            def message_handler(ch, method, properties, body):
                try:
                    # 메시지 디코딩
                    message = body.decode('utf-8')
                    print(f"Message Received: {message}")

                    # 사용자 정의 처리 함수 실행 (비동기 함수 지원)

                    if asyncio.iscoroutinefunction(function):
                        asyncio.run(function(message))
                    else:
                        function(message)

                    # 메시지 처리 완료 확인
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print("ACK")

                except Exception as e:
                    print(f"Message Processing Failed: {e}")
                    # 메시지 거부 (재큐잉 안함)
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            # Consumer 설정
            self.channel.basic_qos(prefetch_count=1)  # 한 번에 하나씩 처리
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=message_handler
            )

            self.channel.start_consuming()

        except KeyboardInterrupt:
            print("\nConsumer Stopped")
            self.channel.stop_consuming()



