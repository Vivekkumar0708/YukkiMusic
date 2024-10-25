#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved

import os
import sys
from typing import Dict, List, Union


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


def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = "/", case_sensitive: bool = False):
    """
    Multilingual command filter for Pyrogram.

    Parameters:
        commands (``str`` | ``list``):
            The command or list of commands as string the filter should look for.
            These should be the keys in your language-specific YAML files.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the filter should look for.
            Defaults to "/" (slash).

        case_sensitive (``bool``, *optional*):
            Pass True if you want your command(s) to be case sensitive. Defaults to False.
    """
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, client, message: Message):
        lang_code = await get_lang(message.chat.id)  # Assuming you have a function to get the user's language
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.commands:
                cmd_variations = get_command(cmd, lang_code)
                if isinstance(cmd_variations, str):
                    cmd_variations = [cmd_variations]

                if not flt.case_sensitive:
                    if not any(without_prefix.lower().startswith(var.lower()) for var in cmd_variations):
                        continue
                else:
                    if not any(without_prefix.startswith(var) for var in cmd_variations):
                        continue

                cmd_used = next(var for var in cmd_variations if without_prefix.lower().startswith(var.lower()))
                without_command = without_prefix[len(cmd_used):].strip()

                message.command = [cmd_used] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_command)
                ]

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return filters.create(
        func,
        "MultilingualCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )