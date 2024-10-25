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
