#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved

import re
import os
import sys
from typing import Union, List
from typing import Dict, List, Union

from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client



from YukkiMusic.utils.database import get_lang

import yaml

languages = {}
commands = {}

languages_present = {}


def get_command(value: str, lang: str = "en") -> Union[str, List[str]]:
    if lang not in commands:
        lang = "en"
    
    return commands[lang].get(value, value)

def command(cmd: str, lang: str = "en"):
    cmds = " ".join([f"/{c}" for c in get_command(cmd, lang)])
    return cmds


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./strings/cmds/"):
    if filename.endswith('.yml'):
        language_code = filename[:-4]
        file_path = os.path.join(commands_dir, filename)
        with open(file_path, 'r', encoding='utf8') as file:
            commands[language_code] = yaml.safe_load(file)

for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except:
        print(
            "There is some issue with the language file inside bot. Please report it to the TheTeamvk at @TheTeamvk on Telegram"
        )
        sys.exit()

if not commands:
    print(
        "There's a problem loading the command files. Please report it to the TheTeamVivek at @TheTeamVivek on Telegram"
    )
    sys.exit()


def command(commands: Union[str, List[str]], prefixes: Union[str, List[str], None] = "/", case_sensitive: bool = False):
    async def func(flt, client: Client, message: Message):
        lang_code = await get_lang(message.chat.id)
        
        if isinstance(commands, str):
            commands_list = [commands]
        else:
            commands_list = commands

        localized_commands = []
        en_commands = []
        for cmd in commands_list:
            localized_cmd = get_command(cmd, lang_code)
            if isinstance(localized_cmd, str):
                localized_commands.append(localized_cmd)
            elif isinstance(localized_cmd, list):
                localized_commands.extend(localized_cmd)
            
            en_cmd = get_command(cmd, "en")
            if isinstance(en_cmd, str):
                en_commands.append(en_cmd)
            elif isinstance(en_cmd, list):
                en_commands.extend(en_cmd)

        username = client.me.username or ""
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        def match_command(cmd, text):
            if flt.prefixes:
                for prefix in flt.prefixes:
                    if text.startswith(prefix):
                        without_prefix = text[len(prefix):]
                        if re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                    flags=re.IGNORECASE if not flt.case_sensitive else 0):
                            return prefix + cmd
            else:
                if re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", text,
                            flags=re.IGNORECASE if not flt.case_sensitive else 0):
                    return cmd
            return None

        all_commands = en_commands + localized_commands if lang_code != "en" else en_commands
        
        for cmd in all_commands:
            matched_cmd = match_command(cmd, text)
            if matched_cmd:
                without_command = re.sub(rf"{matched_cmd}(?:@?{username})?\s?", "", text, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)
                message.command = [matched_cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in re.finditer(r'([^\s"\']+)|"([^"]*)"|\'([^\']*)\'', without_command)
                ]
                return True

        return False

    if prefixes == "" or prefixes is None:
        prefixes = set()
    else:
        prefixes = set(prefixes) if isinstance(prefixes, list) else {prefixes}

    return filters.create(
        func,
        "MultilingualCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )