from fastapi import APIRouter, Depends
from parallelstone_manager.core.dependencies import get_rcon_service, RCONService

router = APIRouter()

@router.post("/start")
def start_server():
    return {"status": "success", "message": "Server started (fake)"}

@router.get("/status") 
async def get_status(rcon: RCONService = Depends(get_rcon_service)):
    is_connected = await rcon.test_connection()
    return {
        "status": "running" if is_connected else "offline", 
        "connected": is_connected
    }

@router.get("/test-connection")
async def test_connection(rcon: RCONService = Depends(get_rcon_service)):
    is_connected = await rcon.test_connection()
    return {"connected": is_connected}

@router.get("/commands")
async def execute_command(cmd: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(cmd)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
