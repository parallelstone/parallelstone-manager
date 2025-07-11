from typing import AsyncGenerator
from fastapi import Depends
from .config import settings
from services.rcon import RCONClient


class RCONService:
    """RCON 서비스 의존성 주입"""
    
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password
        self._client = None
    
    async def get_client(self) -> RCONClient:
        """RCON 클라이언트 반환"""
        if self._client is None:
            self._client = RCONClient(self.host, self.port, self.password)
        return self._client
    
    async def execute_command(self, command: str) -> str:
        """명령어 실행"""
        client = await self.get_client()
        try:
            await client.connect()
            result = await client.send_command(command)
            return result
        finally:
            await client.close()
    
    async def test_connection(self) -> bool:
        """연결 테스트"""
        try:
            result = await self.execute_command("list")
            return True
        except:
            return False


# 전역 RCON 서비스 인스턴스
rcon_service = RCONService(
    host=settings.minecraft_host,
    port=settings.minecraft_port,
    password=settings.minecraft_password
)


async def get_rcon_service() -> RCONService:
    """RCON 서비스 의존성 주입"""
    return rcon_service


async def get_minecraft_config() -> dict:
    """마인크래프트 설정 반환"""
    return {
        "host": settings.minecraft_host,
        "port": settings.minecraft_port,
        "password": settings.minecraft_password
    }