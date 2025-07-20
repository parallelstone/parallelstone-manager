from fastapi import APIRouter, Depends
from parallelstone_manager.core.dependencies import get_rcon_service, RCONService
from parallelstone_manager.core.gamerule import check_rule_value, minecraft_gamerules

router = APIRouter()

@router.post("/start")
def start_server():
    return {"status": "success", "message": "Server started (fake)"}

@router.post("/stop")
def stop_server():
    return {"status": "success", "message": "Server stopped (fake)"}

@router.post("/restart")
def start_server():
    try:
        stop_server()
        start_server()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success", "message": "Server restarted (fake)"}

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

@router.post("/announce")
async def announce(msg: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"say {msg}")
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/gamerule")
async def gamerule(rule: str, value: str, rcon: RCONService = Depends(get_rcon_service)):
    value = value.lower()
    if value == "default":
        value = str(minecraft_gamerules[rule]).lower()

    if check_rule_value(rule, value):
        try:
            result = await rcon.execute_command(f"gamerule {rule} {value}")
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "error": "Input Not Valid"}

