import pika


class RabbitMQConnection:
    def __init__(self, host: str, port: int, username: str, password: str, virtual_host: str = "/"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=pika.PlainCredentials(username=self.username, password=self.password),
                    virtual_host=self.virtual_host
                )
            )
            self.channel = self.connection.channel()
        except Exception as e:
            print(f"RabbitMQ connection error: {e}")
            raise e

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("RabbitMQ connection closed")
            self.connection = None


    def declare_exchange(self,
                         exchange_name: str,
                         exchange_type: str,
                         durable: bool = True,
                         auto_delete: bool = False):
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            durable=durable,
            auto_delete=auto_delete
        )


    def declare_queue(self,
                      queue_name: str,
                      durable: bool = True,
                      auto_delete: bool = False,
                      arguments: dict = None):
        self.channel.queue_declare(
            queue=queue_name,
            durable=durable,
            auto_delete=auto_delete,
            arguments=arguments or {}
        )


    def bind_queue_to_exchange(self,
                   queue_name: str,
                   exchange_name: str,
                   routing_key: str):
        self.channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )


    def setup_pattern(self,
                      exchange_name: str,
                      exchange_type: str,
                      queue_and_keys: list[tuple]
                      ):
        self.declare_exchange(
            exchange_name=exchange_name,
            exchange_type=exchange_type,
        )

        for queue_name, routing_key in queue_and_keys:
            self.declare_queue(queue_name)
            self.bind_queue_to_exchange(queue_name, exchange_name, routing_key)


class NotificationPublisher:
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection
        self.channel = self.connection.channel


    def publish_to_exchange(self, exchange_name: str, routing_key: str, message: str):
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='text/plain',
                content_encoding='utf-8'
            )
        )
        print("[Message published]\n"
              + f" - Exchange: {exchange_name}\n - Routing Key: {routing_key}"
              + f" - Message: {message}")


if __name__ == "__main__":
    from parallelstone_manager.core.config import settings
    
    print(f"RabbitMQ Settings:")
    print(f"Host: {settings.rabbitmq_host}")
    print(f"Port: {settings.rabbitmq_port}")
    print(f"Username: {settings.rabbitmq_username}")
    print(f"Password: {settings.rabbitmq_password}")
    print(f"Virtual Host: {settings.rabbitmq_virtual_host}")
    
    mq = RabbitMQConnection(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )
    mq.connect()
    qnk = [
        ("telegram_queue", "#.telegram.#"),
        ("discord_queue", "#.discord.#"),
        ("slack_queue", "#.slack.#")
    ]
    mq.setup_pattern("notification_router", "topic", qnk)

    pb = NotificationPublisher(mq)

    pb.publish_to_exchange(
        "notification_router",
        "test.telegram",
        "Test Message"
    )
    
    # 다른 패턴도 테스트
    pb.publish_to_exchange(
        "notification_router",
        "telegram",
        "Direct telegram message"
    )
    
    pb.publish_to_exchange(
        "notification_router",
        "anything.telegram.anything",
        "Complex telegram message"
    )
