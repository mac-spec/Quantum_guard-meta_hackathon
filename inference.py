import os
import json
import httpx
import asyncio
from openai import OpenAI
from typing import List, Optional

# Meta Config
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")
ENV_URL = "http://127.0.0.1:8000" 
BENCHMARK = "quantum-guard-v1"

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error if error else 'null'}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_action_from_llm(client: OpenAI, syndrome: list) -> int:
    # Convert list to string to avoid any parsing issues
    s_str = str(syndrome)
    
    prompt = f"""
    You are a Quantum Decoder. Look at the Current Syndrome and pick the matching Action Number.
    
    Current Syndrome: {s_str}
    
    Rules:
    - If Syndrome is [1, 1], your Action is: 1
    - If Syndrome is [1, 0], your Action is: 0
    - If Syndrome is [0, 1], your Action is: 2
    - If Syndrome is [0, 0], you have won.
    
    Reply with ONLY the number (0, 1, or 2). Do not write words.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[{"role": "user", "content": prompt}], 
            temperature=0.0, # CRITICAL: Keeps the model from "guessing"
            max_tokens=2
        )
        text = completion.choices[0].message.content.strip()
        # Find the first number in the response
        for char in text:
            if char.isdigit(): return int(char)
        return 0
    except:
        return 0

async def run_eval_for_task(client, task_id):
    rewards, steps_taken, success, score = [], 0, False, 0.0
    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)
    try:
        # PING_URL/reset check uses POST
        res = httpx.post(f"{ENV_URL}/reset?difficulty={task_id}", json={})
        obs = res.json()
        for step in range(1, 6):
            action = get_action_from_llm(client, obs["syndrome"])
            step_res = httpx.post(f"{ENV_URL}/step", json={"qubit_idx": action})
            data = step_res.json()
            reward, done, obs = data["reward"], data["done"], data
            rewards.append(reward)
            steps_taken = step
            log_step(step=step, action=str(action), reward=reward, done=done, error=None)
            if done:
                success = (reward >= 1.0)
                score = 1.0 if success else max(rewards)
                break
    except Exception as e: print(f"[DEBUG] {task_id} failed: {e}")
    finally: log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    for t_id in ["task_1", "task_2", "task_3", "task_4", "task_5"]:
        await run_eval_for_task(client, t_id)

if __name__ == "__main__":
    asyncio.run(main())