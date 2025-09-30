from fastapi import APIRouter, Depends
from parallelstone_manager.core.dependencies import get_rcon_service, RCONService
from parallelstone_manager.core.gamerule import check_rule_value, minecraft_gamerules
from parallelstone_manager.models.responses import ApiResponse

router = APIRouter()

@router.post("/start")
def start_server():
    return ApiResponse(success=True, message="Server started (fake)")

@router.post("/stop")
def stop_server():
    return ApiResponse(success=True, message="Server stopped (fake)")

@router.post("/restart")
def restart_server():
    try:
        stop_server()
        start_server()
        return ApiResponse(success=True, message="Server restarted (fake)")
    except Exception as e:
        return ApiResponse(success=False, message="Server restart failed", data={"error": str(e)})

@router.get("/status")
async def get_status(rcon: RCONService = Depends(get_rcon_service)):
    is_connected = await rcon.test_connection()
    return ApiResponse(
        success=is_connected,
        message="Server is running" if is_connected else "Server is offline",
        data={"status": "running" if is_connected else "offline", "connected": is_connected}
    )

@router.get("/test-connection")
async def test_connection(rcon: RCONService = Depends(get_rcon_service)):
    is_connected = await rcon.test_connection()
    return ApiResponse(
        success=is_connected,
        message="Connection test successful" if is_connected else "Connection test failed",
        data={"connected": is_connected}
    )

@router.get("/commands")
async def execute_command(cmd: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(cmd)
        return ApiResponse(success=True, message="Command executed successfully", data={"result": result})
    except Exception as e:
        return ApiResponse(success=False, message="Command execution failed", data={"error": str(e)})

@router.post("/announce")
async def announce(msg: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"say {msg}")
        return ApiResponse(success=True, message="Announcement sent successfully", data={"result": result})
    except Exception as e:
        return ApiResponse(success=False, message="Announcement failed", data={"error": str(e)})

@router.post("/gamerule")
async def gamerule(rule: str, value: str, rcon: RCONService = Depends(get_rcon_service)):
    value = value.lower()
    if value == "default":
        value = str(minecraft_gamerules[rule]).lower()

    if check_rule_value(rule, value):
        try:
            result = await rcon.execute_command(f"gamerule {rule} {value}")
            return ApiResponse(success=True, message="Gamerule updated successfully", data={"result": result})
        except Exception as e:
            return ApiResponse(success=False, message="Gamerule update failed", data={"error": str(e)})
    else:
        return ApiResponse(success=False, message="Invalid gamerule value", data={"error": "Input Not Valid"})

