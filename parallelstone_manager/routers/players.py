from fastapi import APIRouter, Depends
from parallelstone_manager.core.dependencies import get_rcon_service, RCONService


router = APIRouter()

@router.get("/") 
async def get_players(rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command("list")
        num_of_players = result.split()[2]
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "running", "player_count": num_of_players}

@router.get("/player_list")
async def get_player_list(rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command("list")
        lst = result.split()
        lst = lst[10:]
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "running", "players": lst}

@router.get("/count")
async def get_players_count():
    try:
        result = await rcon.execute_command("list")
        num_of_players = result.split()[2]
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "running", "player_count": num_of_players}

@router.post("/kick")
async def kick_player(player_name: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"kick {player_name}")
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "running", "msg": result}

