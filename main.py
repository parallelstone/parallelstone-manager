from fastapi import FastAPI

from routers import server, players

app = FastAPI(title="Minecraft API", version="1.0.0")


app.include_router(server.router, prefix="/server", tags=["server"])
app.include_router(players.router, prefix="/players", tags=["players"])

@app.get("/")
def root():
    return {"message": "Hello Minecraft API"}

