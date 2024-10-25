#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import re
import asyncio
import aiohttp
import yt_dlp

from YukkiMusic.utils.formatters import seconds_to_min
from YukkiMusic.utils.exceptions import AssistantErr

class Meta:
    def __init__(self):
        self.regex = r"^(https?:\/\/)?(www\.)?(facebook|fb)\.(com|watch)\S*"
        self.BASE = "https://graph.facebook.com/v16.0/"

    async def valid(self, link: str):
        if re.match(self.regex, link):
            return True
        else:
            return False

    async def info(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False

        ydl_opts = {
            'extract_flat': True,
            'force_generic_extractor': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True
        }
        
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                None, 
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
            )
            
            if not info:
                raise AssistantErr("Unable to fetch video information.")
            
            title = info.get('title', 'Unknown Title')
            duration_in_sec = info.get('duration')
            if duration_in_sec:
                duration = seconds_to_min(duration_in_sec)
            else:
                duration = "Unknown"

            thumbnail = info.get('thumbnail', None)
            vidid = info.get('id', url)

            return (
                title,
                duration,
                thumbnail,
                vidid,
            )

        except Exception as e:
            raise AssistantErr(f"Error fetching information for facebook: {str(e)}")

    async def download(self, url, mystic):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(id)s.%(ext)s',
            'geo_bypass': True,
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
        }
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True)
            )
            downloaded_file = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)
            return downloaded_file
        except Exception as e:
            raise AssistantErr(f"Error downloading facebook video: {str(e)}")