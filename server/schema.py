from pydantic import BaseModel
from typing import List

class ActionRequest(BaseModel):
    # The agent must send an integer: 0, 1, or 2
    qubit_idx: int 

class ObservationResponse(BaseModel):
    # What the agent gets back
    syndrome: List[int]
    reward: float
    done: bool
    info: str