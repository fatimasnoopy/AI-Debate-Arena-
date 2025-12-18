import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Groq (seul API actif)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

# Paramètres communs
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "400"))

# Paramètres du débat
DEBATE_ROUNDS = int(os.getenv("DEBATE_ROUNDS", "3"))
OPENING_LENGTH = int(os.getenv("OPENING_LENGTH", "300"))
REBUTTAL_LENGTH = int(os.getenv("REBUTTAL_LENGTH", "200"))
CONCLUSION_LENGTH = int(os.getenv("CONCLUSION_LENGTH", "300"))
