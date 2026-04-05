import numpy as np

class QuantumEngine:
    def __init__(self):
        self.max_steps = 5
        self.reset("task_1")

    def reset(self, task_id="task_1"):
        self.current_task = task_id
        self.qubits = np.array([0, 0, 0])
        self.steps = 0
        
        if task_id == "task_1": self.qubits[1] = 1
        elif task_id == "task_2": self.qubits[0] = 1; self.qubits[2] = 1
        elif task_id == "task_3": self.qubits[0] = 1
        elif task_id == "task_4": self.qubits = np.array([1, 1, 1])
        else: self.qubits = np.random.choice([0, 1], size=3)
            
        return self.get_observation()

   
    def step(self, qubit_idx):
        if 0 <= qubit_idx < 3:
            self.qubits[qubit_idx] = 1 - self.qubits[qubit_idx]
            self.steps += 1
        
        # We also need to return the new state, reward, and done status
        # to satisfy the app.py call
        obs = self.get_observation()
        reward = self.get_grader_score()
        done = self.check_success() or self.steps >= self.max_steps
        
        return {
            "syndrome": obs,
            "reward": reward,
            "done": done
        }

    def get_observation(self):
        s1 = int(self.qubits[0] ^ self.qubits[1])
        s2 = int(self.qubits[1] ^ self.qubits[2])
        return [s1, s2]

    def get_grader_score(self):
        if np.all(self.qubits == 0): return 1.0
        return 0.5 if sum(self.get_observation()) == 1 else 0.0
        
    def check_success(self):
        return np.all(self.qubits == 0)