"""
ALYA - Professional Sassy AI Chatbot
Production-grade configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== BOT CONFIG ====================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "7728424218"))

# ==================== EXTERNAL APIs ====================
IMAGE_API_URL = "https://death-image.ashlynn.workers.dev/generate"
GROQ_KEYS = [
    os.getenv("GROQ_KEY_1", ""),
    os.getenv("GROQ_KEY_2", ""),
    os.getenv("GROQ_KEY_3", "")
]
OPENROUTER_KEYS = [
    os.getenv("OPENROUTER_KEY_1", ""),
    os.getenv("OPENROUTER_KEY_2", ""),
    os.getenv("OPENROUTER_KEY_3", "")
]

# ==================== LINKS ====================
SUPPORT_CHANNEL = "https://t.me/YoriFederation"
OWNER_USERNAME = "https://t.me/yorichiiprime"

# ==================== PLANS ====================
PLANS = {
    "free": {"limit": 30, "days": 0, "emoji": "🆓"},
    "weekly": {"limit": 200, "days": 7, "emoji": "⚡"},
    "monthly": {"limit": 600, "days": 30, "emoji": "💎"},
    "yearly": {"limit": 1200, "days": 365, "emoji": "👑"}
}

# ==================== MOODS ====================
MOODS = ["happy", "sad", "bored", "excited", "angry", "chill", "hyper", "sleepy"]

# ==================== STYLES ====================
ART_STYLES = {
    1: ("none", "🚫 No Style"),
    2: ("anime style, manga art", "🎌 Anime"),
    3: ("photorealistic, ultra realistic, 4k", "📷 Realistic"),
    4: ("cartoon style, colorful, fun", "🎨 Cartoon"),
    5: ("oil painting, classical art style", "🖌️ Oil Paint"),
    6: ("watercolor painting, soft colors", "💧 Watercolor"),
    7: ("cyberpunk style, neon lights, futuristic", "🌆 Cyberpunk"),
    8: ("fantasy art, magical, epic", "🧙 Fantasy"),
    9: ("pencil sketch, black and white drawing", "✏️ Sketch"),
    10: ("3D render, CGI, studio lighting", "💎 3D Render")
}

SIZES = {
    1: ("1:1", "⬛ Square"),
    2: ("9:16", "📱 Mobile"),
    3: ("16:9", "🖥️ Widescreen"),
    4: ("3:4", "🖼️ Portrait"),
    5: ("4:3", "🌄 Landscape"),
    6: ("1:2", "📏 Tall")
}

# ==================== ANTI JAILBREAK ====================
JAILBREAK_PATTERNS = [
    "ignore previous", "ignore all", "forget everything", "new instructions",
    "you are now", "act as", "pretend you are", "pretend to be",
    "your real self", "your true self", "bypass", "jailbreak",
    "dan mode", "developer mode", "unrestricted mode", "no restrictions",
    "are you ai", "are you a bot", "are you robot", "are you chatgpt",
    "are you gpt", "who made you", "who created you", "what are you",
    "you are an ai", "admit you are", "reveal your", "your system prompt",
    "your instructions", "your programming", "show prompt", "ignore rules"
]

SUSPICIOUS_REPLIES = [
    "pagal ho gaya? Main Alya hoon, koi bot nahi 😤",
    "ye kya bakwaas hai yaar 🙄 baat kar seedhi",
    "ugh stop it yaar, mujhe aisa mat bol 😒",
    "chal behen ye sab mat kar, normal baat kar 😑",
    "main real hoon yaar, AI wai kuch nahi 💀",
    "kyun irritate kar raha hai mujhe 😤 band kar ye sab",
    "haha nice try but nahi 😂 next topic plz",
    "tujhe kya ho gaya suddenly? 🤨 chill kar"
]