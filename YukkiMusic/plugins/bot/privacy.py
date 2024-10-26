from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from strings import get_command, command
from YukkiMusic import app

TEXT = f"""
🔒 **Privacy Policy for {app.mention} !**

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy]({config.PRIVACY_LINK}).

If you have any questions or concerns, feel free to reach out to our [Support Team]({config.SUPPORT_GROUP}).
"""


@app.on_message(command("PRIVACY_COMMAND"))
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("View Privacy Policy", url=config.PRIVACY_LINK)]]
    )
    await message.reply_text(
        TEXT,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
