from fastapi import APIRouter, Depends
from parallelstone_manager.core.dependencies import get_rcon_service, RCONService
from parallelstone_manager.models.responses import ApiResponse


router = APIRouter()

@router.get("/")
async def get_players(rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command("list")
        num_of_players = result.split()[2]
        return ApiResponse(success=True, message="Player count retrieved", data={"player_count": num_of_players})
    except Exception as e:
        return ApiResponse(success=False, message="Failed to get player count", data={"error": str(e)})

@router.get("/player_list")
async def get_player_list(rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command("list")
        lst = result.split()
        lst = lst[10:]
        return ApiResponse(success=True, message="Player list retrieved", data={"players": lst})
    except Exception as e:
        return ApiResponse(success=False, message="Failed to get player list", data={"error": str(e)})


@router.post("/kick")
async def kick_player(player_name: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"kick {player_name}")
        if "No player was found" in result:
            return ApiResponse(success=False, message="Player not found", data={"error": result})
        return ApiResponse(success=True, message="Player kicked successfully", data={"result": result})
    except Exception as e:
        return ApiResponse(success=False, message="Failed to kick player", data={"error": str(e)})

@router.post("/ban")
async def ban_player(player_name: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"ban {player_name}")
        if "That player does not exist" in result:
            return ApiResponse(success=False, message="Player does not exist", data={"error": result})
        return ApiResponse(success=True, message="Player banned successfully", data={"result": result})
    except Exception as e:
        return ApiResponse(success=False, message="Failed to ban player", data={"error": str(e)})


@router.post("/pardon")
async def pardon_player(player_name: str, rcon: RCONService = Depends(get_rcon_service)):
    try:
        result = await rcon.execute_command(f"pardon {player_name}")
        if "That player does not exist" in result:
            return ApiResponse(success=False, message="Player does not exist", data={"error": result})
        return ApiResponse(success=True, message="Player pardoned successfully", data={"result": result})
    except Exception as e:
        return ApiResponse(success=False, message="Failed to pardon player", data={"error": str(e)})

