---
title: Quantum Guard
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: server/app.py
pinned: false
tags:
- openenv
---

# 🛡️ Quantum Guard: AI-Driven Error Correction

This is an OpenEnv-compliant environment for the Meta PyTorch OpenEnv Hackathon. 
It simulates a 3-qubit quantum register and uses a Qwen-72B model to decode bit-flip syndromes.

## 🚀 How to Run
1. Ensure the `HF_TOKEN` is set in your Space Secrets.
2. The environment starts automatically via the `Dockerfile`.
3. Use the `inference.py` script to test the agent's decoding accuracy.