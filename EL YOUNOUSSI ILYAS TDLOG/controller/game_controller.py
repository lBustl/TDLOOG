import uvicorn  # module for running FastAPI web server
from fastapi import FastAPI, Request  # web framework for building APIs
from fastapi.responses import JSONResponse  # for creating JSON responses
from pydantic import BaseModel  # for defining request and response models
from ..model.game import Game  # model for representing a game
from ..services.game_service import GameService  # service for managing game objects

app = FastAPI()  # create FastAPI instance
game_service = GameService()  # create instance of GameService

# define request model for creating a new game
class CreateGameData(BaseModel):
    player_name: str
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

# define endpoint for creating a new game
@app.post("/create-game")
async def create_game(game_data: CreateGameData):
    # delegate to game service to create the game
    return game_service.create_game(game_data.player_name, game_data.min_x,
    game_data.max_x, game_data.min_y,
    game_data.max_y, game_data.min_z,
    game_data.max_z)

# define endpoint for getting a game by its ID
@app.get("/get-game")
async def get_game(game_id: int) -> Game:
    # delegate to game service to get the game
    return game_service.get_game(game_id)

# define request model for joining a game
class JoinGameData(BaseModel):
    game_id: int
    player_name: str

# define endpoint for joining a game
@app.post("/join-game")
async def join_game(game_data: JoinGameData) -> bool:
    # delegate to game service to handle the join request
    return game_service.join_game(game_data.game_id, game_data.player_name)

# define request model for adding a vessel to a game
class AddVesselData(BaseModel):
    game_id: int
    player_name: str
    vessel_type: str
    x: int
    y: int
    z: int

# define endpoint for adding a vessel to a game
@app.post("/add-vessel")
async def add_vessel(game_data: AddVesselData) -> bool:
    # delegate to game service to handle the vessel add request
    return game_service.add_vessel(game_data.game_id, game_data.player_name, game_data.vessel_type, game_data.x,
                                   game_data.y, game_data.z)

# define request model for shooting at a vessel in a game
class ShootAtData(BaseModel):
    game_id: int
    shooter_name: str
    vessel_id: int
    x: int
    y: int
    z: int

# define endpoint for shooting at a vessel in a game

@app.post("/shoot-at")
async def shoot_at(game_data: ShootAtData) -> bool:
    return game_service.shoot_at(game_data.game_id, game_data.shooter_name, game_data.vessel_id, game_data.x,
                                 game_data.y, game_data.z)

@app.get("/game-status")
async def get_game_status(game_id: int, player_name: str) -> str:
    return game_service.get_game_status(game_id, player_name)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"{exc}"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
