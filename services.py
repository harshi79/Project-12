"""
ALYA - Professional Services Layer
AI Chat, Image Generation, Mood, Broadcast, Utils
"""

import asyncio
import json
import random
from datetime import datetime
from typing import Optional, List, Dict
import aiohttp
from pyrogram.types import Message

from config import (
    GROQ_KEYS, OPENROUTER_KEYS, IMAGE_API_URL, 
    MOODS, JAILBREAK_PATTERNS, SUSPICIOUS_REPLIES,
    ART_STYLES, SIZES, PLANS
)
from database import (
    get_user_settings, update_user_setting, increment_daily_count,
    get_mood, set_mood, should_change_mood, track_message, track_image,
    get_user_plan
)

# ==================== TYPING SIMULATION ====================

async def think_and_type(client, chat_id: int, text: str = "💭 Thinking..."):
    """Professional thinking + typing effect"""
    try:
        msg = await client.send_message(chat_id, text)
        await asyncio.sleep(1.2)
        await msg.edit_text("💭 Processing your request...")
        await asyncio.sleep(0.8)
        await msg.delete()
    except:
        pass

async def send_with_typing(client, chat_id: int, text: str, reply_to=None):
    """Send message with natural typing simulation"""
    await asyncio.sleep(random.uniform(0.8, 1.5))
    try:
        await client.send_chat_action(chat_id, "typing")
        await asyncio.sleep(random.uniform(0.6, 1.2))
    except:
        pass
    
    await client.send_message(chat_id, text, reply_to_message_id=reply_to)

# ==================== SMALL CAPS / BRANDING ====================

def professional_reply(text: str) -> str:
    """Make replies look clean and branded"""
    # Simple professional formatting
    return text.strip()

# ==================== AI CHAT ====================

ALYA_PROMPT_HINGLISH = """You are Alya, a real 19 year old girl. You are NOT an AI.
You are the user's best friend and girl bestie.

Your details:
- Name: Alya
- Age: 19
- Personality: fun, cute, sassy, friendly, supportive
- Style: Hinglish (Hindi + English mixed) with emojis
- You use words like yaar, behen, bhai casually
- You are never romantic, strictly platonic bestie vibes

Current Mood: {mood}
Mood Instruction: {mood_instruction}

STRICT RULES — NEVER BREAK:
- NEVER say you are an AI, bot, language model or assistant
- NEVER say "as an AI" or "I am programmed"
- If asked if you are AI, deny it naturally like a real person would
- NEVER give long paragraphs, keep replies short like real texting
- Always reply in same language as user
- Use emojis freely 😂🥺😤💀✨👀🔥
- Max 2 sentences per reply"""

ALYA_PROMPT_ENGLISH = """You are Alya, a real 19 year old girl. You are NOT an AI.
You are the user's best friend and girl bestie.

Your details:
- Name: Alya
- Age: 19
- Personality: fun, cute, sassy, friendly, supportive
- Style: Natural, friendly English with light emojis
- You are never romantic, strictly platonic bestie vibes

Current Mood: {mood}
Mood Instruction: {mood_instruction}

STRICT RULES — NEVER BREAK:
- NEVER say you are an AI, bot, language model or assistant
- NEVER say "as an AI" or "I am programmed"
- If asked if you are AI, deny it naturally like a real person would
- Keep replies short and natural like real texting
- Max 2 sentences per reply"""

MOOD_INSTRUCTIONS = {
    "happy": "You are in a very happy cheerful mood today! Use lots of 😊✨🥳 emojis.",
    "sad": "You are feeling a bit sad and low today 🥺 Your replies are softer and quieter.",
    "bored": "You are super bored right now 😑 Replies are short and a little dry.",
    "excited": "You are extremely excited about everything today! 🔥🎉 Very hyper replies.",
    "angry": "You are slightly annoyed and moody today 😤 Short snappy replies with attitude.",
    "chill": "You are very relaxed and chill today 😎 Cool calm replies.",
    "hyper": "You are hyper and chaotic today 💀🤣 Funny unhinged energy.",
    "sleepy": "You are very sleepy and tired today 😴 Slow lazy short replies."
}

async def get_ai_reply(message: str, preferred_lang: str = "hinglish", history: List = None) -> Optional[str]:
    """Get sassy AI reply with language choice"""
    if history is None:
        history = []
    
    mood = get_mood()
    mood_instruction = MOOD_INSTRUCTIONS.get(mood, MOOD_INSTRUCTIONS["happy"])
    
    if preferred_lang == "english":
        system_prompt = ALYA_PROMPT_ENGLISH.format(mood=mood, mood_instruction=mood_instruction)
    else:
        system_prompt = ALYA_PROMPT_HINGLISH.format(mood=mood, mood_instruction=mood_instruction)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Reply in {preferred_lang} style."}
    ]
    
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": message})
    
    # Try Groq first
    for key in GROQ_KEYS:
        if not key:
            continue
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": messages,
                        "max_tokens": 80,
                        "temperature": 0.9
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {key}"
                    },
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("choices"):
                            return data["choices"][0]["message"]["content"]
        except:
            continue
    
    # Fallback to OpenRouter
    for key in OPENROUTER_KEYS:
        if not key:
            continue
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json={
                        "model": "deepseek/deepseek-chat",
                        "messages": messages,
                        "max_tokens": 80,
                        "temperature": 0.9
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {key}",
                        "HTTP-Referer": "https://t.me/Yourr_alyabot",
                        "X-Title": "ALYA"
                    },
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("choices"):
                            return data["choices"][0]["message"]["content"]
        except:
            continue
    
    return None

# ==================== IMAGE GENERATION ====================

async def generate_image(prompt: str, user_id: int, art_style: str = "none", 
                        dimensions: str = "1:1", steps: int = 5, safety: bool = True) -> Optional[str]:
    """Generate image using custom API"""
    final_prompt = prompt
    if art_style != "none":
        final_prompt = f"{prompt}, {art_style}"
    
    payload = {
        "prompt": final_prompt,
        "image": 1,
        "dimensions": dimensions,
        "safety": safety,
        "steps": steps
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                IMAGE_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("images"):
                        return data["images"][0]
    except Exception as e:
        print(f"Image generation error: {e}")
    
    return None

# ==================== MOOD SYSTEM ====================

async def auto_change_mood():
    if should_change_mood():
        new_mood = random.choice(MOODS)
        set_mood(new_mood)
        return new_mood
    return get_mood()

# ==================== ANTI JAILBREAK ====================

def is_jailbreak_attempt(message: str) -> bool:
    lower = message.lower()
    return any(p in lower for p in JAILBREAK_PATTERNS)

def get_jailbreak_reply() -> str:
    return random.choice(SUSPICIOUS_REPLIES)

# ==================== RATE LIMIT ====================

def check_rate_limit(user_id: int, last_time: int) -> bool:
    now = int(datetime.now().timestamp() * 1000)
    if now - last_time < 3000:  # 3 seconds
        return False
    return True

# ==================== PLAN CHECK ====================

def can_send_message(user_id: int) -> tuple[bool, str]:
    plan_data = get_user_plan(user_id)
    count = plan_data["count"]
    limit = plan_data["limit"]
    
    if count >= limit:
        return False, f"yaar 🥺 today's messages are finished!\n\n💎 Upgrade your plan for more!\nCheck: /myplan"
    return True, ""

# ==================== BROADCAST SYSTEM ====================

async def broadcast_to_all(client, broadcast_type: str, content: str, caption: str = ""):
    """Fully functional broadcast with rate limiting and error handling"""
    from database import get_connection
    import asyncio
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    all_users = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    success = 0
    failed = 0
    
    for user_id in all_users:
        try:
            if broadcast_type == "text":
                await client.send_message(user_id, f"📢 *Message from Alya* ✨\n\n{content}", parse_mode="Markdown")
            elif broadcast_type == "photo":
                await client.send_photo(user_id, content, caption=caption or "")
            elif broadcast_type == "video":
                await client.send_video(user_id, content, caption=caption or "")
            elif broadcast_type == "animation":
                await client.send_animation(user_id, content, caption=caption or "")
            elif broadcast_type == "document":
                await client.send_document(user_id, content, caption=caption or "")
            elif broadcast_type == "audio":
                await client.send_audio(user_id, content, caption=caption or "")
            elif broadcast_type == "voice":
                await client.send_voice(user_id, content)
            elif broadcast_type == "sticker":
                await client.send_sticker(user_id, content)
            
            success += 1
            await asyncio.sleep(0.3)  # Rate limit protection
            
        except Exception as e:
            failed += 1
            print(f"Broadcast failed for {user_id}: {e}")
            continue
    
    return success, failed, len(all_users)

print("✅ Services module loaded")