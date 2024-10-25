import asyncio
import os
import re
import json
from typing import Dict, Union

import aiohttp
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

from YukkiMusic.utils.exceptions import AssistantErr
from YukkiMusic.utils.formatters import seconds_to_min

class MetaApi:
    def __init__(self):
        self.regex = {
            "facebook": r"(?:https?:\/\/)?(?:www\.|web\.|m\.)?facebook\.com\/(?:video\.php\?v=\d+|.*?\/videos\/\d+)|fb\.watch\/\w+",
            "instagram": r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([^\/?#&]+)"
        }
        self.base_url = {
            "facebook": "https://www.facebook.com/",
            "instagram": "https://www.instagram.com/"
        }

    async def valid(self, link: str, platform: str) -> bool:
        if re.search(self.regex[platform], link):
            return True
        return False

    async def download(self, url: str, platform: str) -> Dict[str, Union[str, int]]:
        if platform == "facebook":
            return await self.facebook(url)
        elif platform == "instagram":
            return await self.instagram(url)
        raise AssistantErr("Unsupported platform")

    async def facebook(self, url: str) -> Dict[str, Union[str, int]]:
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
            }
            loop = asyncio.get_running_loop()
            with YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(None, ydl.extract_info, url, False)
                filepath = ydl.prepare_filename(info)
                await loop.run_in_executor(None, ydl.download, [url])

            return {
                "title": info['title'],
                "duration": seconds_to_min(info['duration']),
                "duration_sec": info['duration'],
                "thumbnail": info.get('thumbnail'),
                "filepath": filepath,
                "url": url
            }
        except Exception as e:
            raise AssistantErr(f"Error downloading Facebook video: {str(e)}")

    async def instagram(self, url: str) -> Dict[str, Union[str, int]]:
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
            }
            loop = asyncio.get_running_loop()
            with YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(None, ydl.extract_info, url, False)
                filepath = ydl.prepare_filename(info)
                await loop.run_in_executor(None, ydl.download, [url])

            return {
                "title": info['title'],
                "duration": seconds_to_min(info.get('duration', 0)),
                "duration_sec": info.get('duration', 0),
                "thumbnail": info.get('thumbnail'),
                "filepath": filepath,
                "url": url
            }
        except Exception as e:
            raise AssistantErr(f"Error downloading Instagram video: {str(e)}")