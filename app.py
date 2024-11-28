from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from starlette.requests import Request


# Import the TeekoPlayer class
from game import TeekoPlayer
ai_difficulty = 3  # Default to Beginner

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Cache-Control"],
)


@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
    return response

# Initialize the AI with the default difficulty
ai = TeekoPlayer(depth=ai_difficulty)


# Models
class MoveRequest(BaseModel):
    move: List[List[Optional[int]]]


class MoveResponse(BaseModel):
    board: List[List[str]]
    move: List[List[Optional[int]]]
    turn: str
    game_status: str
    winner: Optional[str]


class GameStateResponse(BaseModel):
    board: List[List[str]]
    game_status: str
    turn: str
    opponent_piece: str
    winner: Optional[str]

class DifficultyRequest(BaseModel):
    difficulty: str


@app.get("/", response_model=GameStateResponse)
async def get_game_state():
    global ai

    game_value = ai.game_value(ai.board)

    # Check if the game is over or draw condition is met
    if game_value == 0 and ai.move_count >= 30:
        game_status = "over"
        winner = "Draw"
    else:
        game_status = "ongoing" if game_value == 0 else "over"
        winner = "AI" if game_value == 1 else "Opponent" if game_value == -1 else None

    # Count pieces to determine whose turn it is (black goes first)
    num_black = sum(row.count(ai.pieces[0]) for row in ai.board)
    num_red = sum(row.count(ai.pieces[1]) for row in ai.board)
    turn = ai.pieces[0] if num_black == num_red else ai.pieces[1]

    # Translate to "AI" or "Opponent" based on the current piece
    turn = "None" if game_status == "over" else ("AI" if turn == ai.my_piece else "Opponent")

    return {
        "board": ai.board,
        "game_status": game_status,
        "turn": turn,
        "opponent_piece": ai.opp,
        "winner": winner,
    }


@app.post("/ai-move/", response_model=MoveResponse)
async def ai_move():
    global ai

    # Ensure the game is not over
    game_value = ai.game_value(ai.board)
    if game_value != 0:
        raise HTTPException(status_code=400, detail="Game is already over.")

    # Check for draw condition
    if ai.move_count >= 30:
        return {
            "board": ai.board,
            "move": [],
            "turn": "None",
            "game_status": "over",
            "winner": "Draw"
        }

    # Determine the current turn explicitly
    num_black = sum(row.count(ai.pieces[0]) for row in ai.board)
    num_red = sum(row.count(ai.pieces[1]) for row in ai.board)
    current_turn_piece = ai.pieces[0] if num_black == num_red else ai.pieces[1]
    if current_turn_piece != ai.my_piece:
        raise HTTPException(status_code=400, detail="It's not AI's turn!")

    # AI makes its move
    move = ai.make_move(ai.board)
    ai.place_piece(move, ai.my_piece)

    # Determine game status and winner
    game_value = ai.game_value(ai.board)
    game_status = "over" if game_value != 0 else "ongoing"
    winner = "AI" if game_value == 1 else "Opponent" if game_value == -1 else None

    # Check for draw condition again after the AI's move
    if ai.move_count >= 30 and winner is None:
        winner = "Draw"
        game_status = "over"

    turn = "None" if game_status == "over" else "Opponent"

    return {
        "board": ai.board,
        "move": move,
        "turn": turn,
        "game_status": game_status,
        "winner": winner,
    }


@app.post("/opponent-move/", response_model=MoveResponse)
async def opponent_move(request: MoveRequest):
    global ai
    move = request.move

    # Check for draw condition
    if ai.move_count >= 30:
        return {
            "board": ai.board,
            "move": [],
            "turn": "None",
            "game_status": "over",
            "winner": "Draw"
        }

    try:
        ai.opponent_move(move)

        # Determine game status and winner
        game_value = ai.game_value(ai.board)
        game_status = "over" if game_value != 0 else "ongoing"
        winner = "AI" if game_value == 1 else "Opponent" if game_value == -1 else None

        # Check for draw condition again after the opponent's move
        if ai.move_count >= 30 and winner is None:
            winner = "Draw"
            game_status = "over"

        turn = "None" if game_status == "over" else "AI"

        return {
            "board": ai.board,
            "move": move,
            "turn": turn,
            "game_status": game_status,
            "winner": winner,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/set-difficulty/")
async def set_difficulty(request: DifficultyRequest):
    global ai, ai_difficulty

    difficulty_map = {
        "beginner": 3,
        "intermediate": 4,
        "expert": 5,
    }

    if request.difficulty not in difficulty_map:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")

    ai_difficulty = difficulty_map[request.difficulty]
    ai.set_difficulty(ai_difficulty)

    print(f"AI difficulty updated to {ai_difficulty} ({request.difficulty})")

    return {"message": f"Difficulty set to {request.difficulty} (depth {ai_difficulty})"}


@app.post("/reset/")
async def reset_game():
    global ai
    ai = TeekoPlayer(depth=ai_difficulty)
    return {
        "board": ai.board,
        "turn": "AI",
        "winner": None,
    }