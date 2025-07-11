from fastapi import APIRouter

router = APIRouter()

@router.get("/") 
def get_players():
    return {"status": "running", "player_count": 5}

@router.get("/count") 
def get_players_count():
    return {"status": "running", "player_count": 5}

@router.post("/kick/{player_name}") 
def kick_player():
    # Kick player
    return {"status": "running", "player_count": 5}

