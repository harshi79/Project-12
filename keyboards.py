"""
ALYA - Professional Keyboards
Clean inline and reply keyboards
"""

from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from config import PLANS, ART_STYLES, SIZES

# ==================== USER KEYBOARDS ====================

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🗑️ Clear My Data"), KeyboardButton("💎 Buy Plan")],
            [KeyboardButton("👤 My Profile"), KeyboardButton("💭 Alya Mood")],
            [KeyboardButton("⚙️ My Settings"), KeyboardButton("🌐 Language")],
            [KeyboardButton("📊 My Plan"), KeyboardButton("❓ Help")],
            [KeyboardButton("💎 Support Dev")]
        ],
        resize_keyboard=True
    )

def settings_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📐 Change Size", callback_data="set_size")],
        [InlineKeyboardButton("🎨 Change Style", callback_data="set_style")],
        [InlineKeyboardButton("🔢 Change Steps", callback_data="set_steps")],
        [InlineKeyboardButton("🔞 Toggle NSFW", callback_data="toggle_nsfw")],
        [InlineKeyboardButton("« Back", callback_data="back_to_menu")]
    ])

def plans_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Buy Plan — Contact Admin", url="https://t.me/yorichiiprime")]
    ])

def fun_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Roll Dice", callback_data="dice_roll")],
        [InlineKeyboardButton("🎯 Throw Dart", callback_data="dart_roll")],
        [InlineKeyboardButton("🏀 Basketball", callback_data="basket_roll")]
    ])

def support_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ 1 Star", callback_data="pay_1")],
        [InlineKeyboardButton("⭐ 10 Stars", callback_data="pay_10")],
        [InlineKeyboardButton("⭐ 50 Stars", callback_data="pay_50")],
        [InlineKeyboardButton("⭐ 100 Stars", callback_data="pay_100")],
        [InlineKeyboardButton("⭐ 500 Stars", callback_data="pay_500")]
    ])

# ==================== ADMIN KEYBOARDS ====================

def admin_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📊 Stats"), KeyboardButton("📢 Broadcast")],
            [KeyboardButton("🖼️ Add Pics"), KeyboardButton("🎭 Add Stickers")],
            [KeyboardButton("📸 View Pics"), KeyboardButton("🎪 View Stickers")],
            [KeyboardButton("🚫 Block User"), KeyboardButton("✅ Unblock User")],
            [KeyboardButton("📺 Add Channel"), KeyboardButton("❌ Remove Channel")],
            [KeyboardButton("👥 All Users"), KeyboardButton("📤 Export Users")],
            [KeyboardButton("📥 Import Users"), KeyboardButton("💎 Give Plan")]
        ],
        resize_keyboard=True
    )

def broadcast_confirm_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes Send!", callback_data="broadcast_confirm"),
            InlineKeyboardButton("❌ Cancel", callback_data="broadcast_cancel")
        ]
    ])

def verify_join_keyboard(channels):
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(f"👉 Join {ch['name']}", url=ch['link'])])
    buttons.append([InlineKeyboardButton("✅ I Joined — Verify Me!", callback_data="verify_join")])
    return InlineKeyboardMarkup(buttons)

# ==================== SIZE & STYLE PICKERS ====================

def size_picker_keyboard():
    buttons = []
    for num, (value, name) in SIZES.items():
        buttons.append([InlineKeyboardButton(f"{name} ({value})", callback_data=f"size_{num}")])
    return InlineKeyboardMarkup(buttons)

def style_picker_keyboard():
    buttons = []
    for num, (value, name) in ART_STYLES.items():
        buttons.append([InlineKeyboardButton(name, callback_data=f"style_{num}")])
    return InlineKeyboardMarkup(buttons)

# ==================== HELP KEYBOARDS ====================

def help_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 User Commands", callback_data="help_user")],
        [InlineKeyboardButton("👑 Developer Commands", callback_data="help_dev")],
        [InlineKeyboardButton("🎮 Fun & Games", callback_data="help_fun")]
    ])

print("✅ Keyboards module loaded")