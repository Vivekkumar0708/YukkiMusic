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
from typing import Tuple, Optional
from yt_dlp import YoutubeDL
from YukkiMusic.utils.exceptions import AssistantErr

class MetaApi:
    def __init__(self):
        # Updated regex to match Instagram URLs
        self.regex = r"^(https?:\/\/)?(www\.)?(instagram)\.(com|tv)\/(?:p|reel|tv)\/([^/?#&]+)"
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'geo_bypass': True,
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
        }

    async def valid(self, link: str) -> bool:
        """Validate if the URL is an Instagram post/reel."""
        return bool(re.match(self.regex, link))

    async def info(self, url: str) -> Tuple[str, str, str, str]:
        """Get information about Instagram media."""
        if not await self.valid(url):
            raise AssistantErr("Invalid Instagram URL")

        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                duration_min = f"{duration // 60}:{duration % 60:02d}"  # Convert to MM:SS
                thumbnail = info.get('thumbnail', None)
                vidid = info.get('id', url)

                return title, duration_min, thumbnail, vidid

        except Exception as e:
            raise AssistantErr(f"Error fetching information for Instagram: {str(e)}")

    async def download(self, url: str) -> str:
        """Download media from Instagram."""
        if not await self.valid(url):
            raise AssistantErr("Invalid Instagram URL")

        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        except Exception as e:
            raise AssistantErr(f"Error downloading Instagram media: {str(e)}")