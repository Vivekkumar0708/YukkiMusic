from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import json
import os
from datetime import datetime
import config
from strings import get_command
from YukkiMusic import app
from config import BANNED_USERS
from YukkiMusic.utils.database import (
    delete_playlist,
    delete_authuser,
    delete_served_user,
    get_playlist_names,
    get_authuser_names,
    is_served_user,
    get_playlist,
    get_lang,
)

TEXT = f"""
🔒 **Privacy Policy for {app.mention}**

Choose an option below to:
- View our Privacy Policy
- Retrieve your data
- Delete your data
- Close

Your privacy matters to us. For any questions, contact our [Support Team]({config.SUPPORT_GROUP}).
"""
PRIVACY_SECTIONS = {
    "collect": """
**What Information We Collect**

• Basic Telegram user data (ID, username)
• Chat/Group IDs where the bot is used
• Command usage and interactions
• Playlists and music preferences
• Voice chat participation data
• User settings and configurations
""",

    "why": """
**Why We Collect It**

• To provide music streaming services
• To maintain user playlists
• To process voice chat requests
• To manage user permissions
• To improve bot features
• To prevent abuse and spam
""",

    "do": """
**What We Do**

• Store data securely in encrypted databases
• Process music requests and streams
• Maintain user preferences
• Monitor for proper functionality
• Delete temporary files after use
• Implement security measures
""",

    "donot": """
**What We Don't Do**

• Share your data with third parties
• Store unnecessary personal information
• Keep data longer than needed
• Use data for marketing
• Track users across platforms
• Sell any user information
""",

    "rights": """
**Your Rights**

• Access your stored data
• Request data deletion
• Modify your settings
• Opt-out of data collection
• Report privacy concerns
• Contact support for help
"""
}

@app.on_message(command("PRIVACY_COMMAND") & ~BANNED_USERS)
async def privacy_menu(client, message: Message):
    """Main privacy menu with 4 buttons"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Privacy Policy", callback_data="show_privacy_sections")],
        [InlineKeyboardButton("Retrieve Data", callback_data="retrieve_data")],
        [InlineKeyboardButton("Delete Data", callback_data="delete_data")],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])
    await message.reply_text(TEXT, reply_markup=keyboard, disable_web_page_preview=True)

@app.on_callback_query(filters.regex("show_privacy_sections") & ~BANNED_USERS)
async def show_privacy_sections(client, callback_query):
    """Show detailed privacy policy sections"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("What We Collect", callback_data="privacy_collect")],
        [InlineKeyboardButton("Why We Collect", callback_data="privacy_why")],
        [InlineKeyboardButton("What We Do", callback_data="privacy_do")],
        [InlineKeyboardButton("What We Don't Do", callback_data="privacy_donot")],
        [InlineKeyboardButton("Your Rights", callback_data="privacy_rights")],
        [InlineKeyboardButton("Back", callback_data="privacy_back")],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])
    await callback_query.edit_message_text(
        "**Privacy Policy Sections**\n\nSelect a section to learn more:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("privacy_") & ~BANNED_USERS)
async def privacy_section_callback(client, callback_query):
    """Handle privacy section callbacks"""
    section = callback_query.data.split("_")[1]
    
    if section == "back":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Privacy Policy", callback_data="show_privacy_sections")],
            [InlineKeyboardButton("Retrieve Data", callback_data="retrieve_data")],
            [InlineKeyboardButton("Delete Data", callback_data="delete_data")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        return await callback_query.edit_message_text(TEXT, reply_markup=keyboard)

    if section in PRIVACY_SECTIONS:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Sections", callback_data="show_privacy_sections")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await callback _query.edit_message_text(
            PRIVACY_SECTIONS[section],
            reply_markup=keyboard
        )