from fastapi import FastAPI
import subprocess
import os
from typing import List
from contextlib import asynccontextmanager

from parallelstone_manager.routers import server, players
from parallelstone_manager.core.config import settings
from parallelstone_manager.core.dependencies import rcon_service
from parallelstone_manager.services.rabbitmq import RabbitMQConnection, NotificationPublisher

# 전역 변수로 RabbitMQ 연결 관리
rabbitmq_connection = None
rabbitmq_publisher = None

def start_consumer_processes():
    """모든 Consumer 프로세스 시작"""
    consumer_processes = []
    
    # Consumer 모듈 목록
    consumer_modules = [
        "parallelstone_manager.consumers.telegram_sender",
        "parallelstone_manager.consumers.discord_sender",
        "parallelstone_manager.consumers.slack_sender",
    ]
    
    for module in consumer_modules:
        try:
            # 가상환경의 python 경로 사용
            python_path = os.path.join(os.getcwd(), ".venv", "bin", "python")
            if not os.path.exists(python_path):
                python_path = "python"  # 가상환경이 없으면 시스템 python 사용
            
            # -m 옵션으로 모듈 실행
            process = subprocess.Popen(
                [python_path, "-m", module],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            consumer_processes.append(process)
            print(f"{module} 프로세스 시작됨 (PID: {process.pid})")
        except Exception as e:
            print(f"{module} 프로세스 시작 실패: {e}")
    
    return consumer_processes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 라이프사이클 관리"""
    # Startup
    global rabbitmq_connection, rabbitmq_publisher
    consumer_processes = []
    
    # RabbitMQ 연결 초기화
    rabbitmq_connection = RabbitMQConnection(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtual_host=settings.rabbitmq_virtual_host
    )
    
    try:
        rabbitmq_connection.connect()
        
        # Exchange와 Queue 설정
        queue_bindings = [
            ("telegram_queue", "#.telegram.#"),
            ("discord_queue", "#.discord.#"),
            ("slack_queue", "#.slack.#")
        ]
        rabbitmq_connection.setup_pattern("notification_router", "topic", queue_bindings)
        
        # Publisher 초기화
        rabbitmq_publisher = NotificationPublisher(rabbitmq_connection)
        
        # 모든 Consumer 프로세스 시작
        consumer_processes = start_consumer_processes()
        
        print("RabbitMQ 및 Consumer 초기화 완료")
        
    except Exception as e:
        print(f"RabbitMQ 초기화 실패: {e}")

    try:
        await rcon_service.connect()
        print(f"RCON Connection Successful")
    except Exception as e:
        print(f"RCON Connection Failed: {e}")
    yield  # 여기서 앱이 실행됨

    # Shutdown
    print("애플리케이션 종료 중...")

    # RCON 연결 종료
    try:
        await rcon_service.disconnect()
        print(f"RCON Connection Closed")
    except Exception as e:
        print(f"RCON Connection Closed: {e}")

    # RabbitMQ 연결 종료
    if rabbitmq_connection:
        try:
            rabbitmq_connection.disconnect()
            print("RabbitMQ 연결 종료")
        except Exception as e:
            print("RabbitMQ 연결 종료됨", e)


    # Consumer 프로세스들 종료
    for process in consumer_processes:
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"Consumer 프로세스 종료됨 (PID: {process.pid})")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Consumer 프로세스 강제 종료됨 (PID: {process.pid})")
        except Exception as e:
            print(f"Consumer 프로세스 종료 실패: {e}")


app = FastAPI(title="Minecraft API", version="1.0.0", lifespan=lifespan)

app.include_router(server.router, prefix="/server", tags=["server"])
app.include_router(players.router, prefix="/players", tags=["players"])

@app.get("/")
def root():
    return {"message": "Hello Minecraft API"}

