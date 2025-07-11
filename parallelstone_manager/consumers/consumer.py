import pika
import asyncio

class BaseConsumer:
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
                    credentials=pika.PlainCredentials(self.username, self.password),
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
    
    def run_consumer(self, consumer_name: str, queue_name: str, handler_function):
        """Consumer 실행 (main.py에서 사용)"""
        if self.connect():
            print(f"{consumer_name} consumer 시작됨")
            self.consume_queue(queue_name, handler_function)
        else:
            print(f"{consumer_name} consumer 연결 실패")
    
    @classmethod
    def create_and_run(cls, consumer_name: str, queue_name: str, handler_function, 
                      host: str, port: int, username: str, password: str, virtual_host: str = "/"):
        """Consumer 생성 및 실행 (팩토리 메서드)"""
        consumer = cls(host, port, username, password, virtual_host)
        consumer.run_consumer(consumer_name, queue_name, handler_function)



