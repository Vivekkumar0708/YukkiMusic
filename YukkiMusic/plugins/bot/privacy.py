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

PRIVACY_COMMAND = get_command("PRIVACY_COMMAND")

TEXT = f"""
🔒 **Privacy Policy for {app.mention}**

Choose an option below to:
- View our Privacy Policy
- Retrieve your data
- Delete your data
- Cancel

Your privacy matters to us. For any questions, contact our [Support Team]({config.SUPPORT_GROUP}).
"""

@app.on_message(command(PRIVACY_COMMAND) & ~BANNED_USERS)
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Privacy Policy", callback_data="view_privacy")],
        [InlineKeyboardButton("Retrieve Data", callback_data="retrieve_data")],
        [InlineKeyboardButton("Delete Data", callback_data="delete_data")],
        [InlineKeyboardButton("Cancel", callback_data="close")]
    ])
    await message.reply_text(TEXT, reply_markup=keyboard, disable_web_page_preview=True)

@app.on_callback_query(filters.regex("view_privacy") & ~BANNED_USERS)
async def privacy_policy(client, callback_query):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Back", callback_data="privacy_back"),
        InlineKeyboardButton("Close", callback_data="close")
    ]])
    await callback_query.edit_message_text(
        f"**Privacy Policy**\n\nRead our full privacy policy here: [Privacy Policy]({config.PRIVACY_LINK})",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

@app.on_callback_query(filters.regex("retrieve_data") & ~BANNED_USERS)
async def retrieve_data(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer("Preparing your data file...")
    
    user_data = {
        "user_id": user_id,
        "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": {
            "playlists": [],
            "authorized_chats": [],
            "user_settings": {}
        }
    }
    
    try:
        if not await is_served_user(user_id):
            user_data["status"] = "No data found for this user"
        else:
            user_data["status"] = "Active user"
            playlists = await get_playlist_names(user_id)
            if playlists:
                for playlist in playlists:
                    playlist_data = await get_playlist(user_id, playlist)
                    user_data["data"]["playlists"].append({
                        "name": playlist,
                        "content": playlist_data
                    })
            
            auth_chats = await get_authuser_names(user_id)
            if auth_chats:
                user_data["data"]["authorized_chats"] = auth_chats
            
            user_data["data"]["user_settings"] = {
                "language": await get_lang(user_id),
            }
        
        file_path = os.path.join("downloads", f"user_data_{user_id}.json")
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)
        
        await callback_query.message.reply_document(
            document=file_path,
            caption="Here's your requested data export. This file contains all your stored information in our bot.",
            file_name=f"user_data_export_{user_id}.json",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="privacy_back"),
                InlineKeyboardButton("Close", callback_data="close")
            ]])
        )
        
        try:
            os.remove(file_path)
        except:
            pass
        
        await callback_query.edit_message_text(
            "✅ Your data has been exported successfully.\nPlease check the file sent above.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="privacy_back"),
                InlineKeyboardButton("Close", callback_data="close")
            ]])
        )
        
    except Exception as e:
        print(f"Error exporting user data: {str(e)}")
        await callback_query.edit_message_text(
            "❌ An error occurred while exporting your data.\nPlease try again later or contact support.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="privacy_back"),
                InlineKeyboardButton("Close", callback_data="close")
            ]])
        )

@app.on_callback_query(filters.regex("delete_data") & ~BANNED_USERS)
async def delete_data(client, callback_query):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚠️ Confirm Delete", callback_data="confirm_delete"),
        InlineKeyboardButton("Cancel", callback_data="privacy_back")
    ]])
    
    await callback_query.edit_message_text(
        "⚠️ **Are you sure you want to delete your data?**\n\n"
        "This will delete:\n"
        "- Your playlists\n"
        "- Your auth permissions\n"
        "- Your user records\n\n"
        "Note: This action cannot be undone!\n"
        "Banned status and blacklisted chat data will be preserved for moderation purposes.",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("confirm_delete") & ~BANNED_USERS)
async def confirm_delete(client, callback_query):
    user_id = callback_query.from_user.id
    deleted = False
    
    try:
        playlists = await get_playlist_names(user_id)
        for playlist in playlists:
            await delete_playlist(user_id, playlist)
        
        auth_chats = await get_authuser_names(user_id)
        for chat in auth_chats:
            await delete_authuser(user_id, chat)
        
        await delete_served_user(user_id)
        
        deleted = True
    except Exception as e:
        print(f"Error deleting user data: {str(e)}")
    
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Back", callback_data="privacy_back"),
        InlineKeyboardButton("Close", callback_data="close")
    ]])
    
    if deleted:
        text = "✅ Your data has been successfully deleted.\n\nNote: Banned status and blacklisted chat data have been preserved for moderation purposes."
    else:
        text = "❌ An error occurred while deleting your data.\nPlease try again later or contact support."
    
    await callback_query.edit_message_text(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("privacy_back") & ~BANNED_USERS)
async def privacy_back(client, callback_query):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Privacy Policy", callback_data="view_privacy")],
        [InlineKeyboardButton("Retrieve Data", callback_data="retrieve _data")],
        [InlineKeyboardButton("Delete Data", callback_data="delete_data")],
        [InlineKeyboardButton("Cancel", callback_data="close")]
    ])
    
    await callback_query.edit_message_text(TEXT, reply_markup=keyboard)