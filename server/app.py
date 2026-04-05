from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .engine import QuantumEngine

app = FastAPI()
engine = QuantumEngine()

class StepRequest(BaseModel):
    qubit_idx: int

@app.post("/reset") # MANDATORY: Must be POST for the validator script
async def reset_env(difficulty: str = "task_1"):
    state = engine.reset(difficulty)
    return {"syndrome": state, "message": f"Environment reset to {difficulty}"}

@app.post("/step")
async def step_env(request: StepRequest):
    # Call the engine
    result = engine.step(request.qubit_idx)
    
    # Force everything to be standard Python types (FastAPI likes this better)
    return {
        "syndrome": [int(s) for s in result["syndrome"]],
        "reward": float(result["reward"]),
        "done": bool(result["done"])
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
if __name__ == "__main__":  
    main() 