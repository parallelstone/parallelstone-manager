from parallelstone_manager.core.config import settings
from parallelstone_manager.services.rcon import RCONClient


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


    async def connect(self):
        client = await self.get_client()
        await client.connect()
        return client

    async def disconnect(self):
        client = await self.get_client()
        await client.close()
        self._client = None
    
    async def execute_command(self, command: str) -> str:
        """명령어 실행"""
        client = await self.get_client()
        if not await client.is_connected():
            print("RCON connection lost. Reconnecting...")
            await self.connect()

        try:
            result = await client.send_command(command)
            return result
        except:
            await self.connect()
            result = await client.send_command(command)
            return result

    
    async def test_connection(self) -> bool:
        """연결 테스트"""
        return await self._client.is_connected()



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