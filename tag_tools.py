import json
import os
import platform
import re

CONST_DIRLIM = "/"
if platform.system() == "windows":
    CONST_DIRLIM = "\\"


class Tag:
    def __init__(self, json, id=None, alias=False):
        if not id:
            id = json["id"]
        self.parent_id = json["id"]
        self.id = id
        self.is_alias = alias
        self.translations = json["translations"]

        if self.is_alias:
            self.localisation = json["aliases"][self.id]["localisation"]
            self.name = json["aliases"][self.id][self.localisation]
            return

        self.localisation = json["defaultLocalisation"]
        self.name = json["translations"][self.localisation]


class TagTools:
    tags = []

    @classmethod
    def find(cls, t):
        for tag in cls.tags:
            # Check against translations
            for localisation, translation in tag["translations"].items():
                if translation.lower() == t.lower():
                    return Tag(tag)

            # Check against aliases
            # This is fucking gross...
            for id, alias in tag["aliases"].items():
                for key, value in alias.items():
                    if key == "localisation" or key == "trueAlias":
                        continue

                    if value.lower() == t.lower():
                        if alias["trueAlias"]:
                            return Tag(tag, id=id, alias=True)
                        return Tag(tag)

            # Check against alternate spellings
            for alternate_spelling in tag["alternateSpellings"]:
                if bool(re.match(alternate_spelling["regex"], t)):
                    target = alternate_spelling["target"]

                    if (
                        target == "alias"
                        and tag["aliases"][alternate_spelling["id"]]["trueAlias"]  # noqa: W503
                    ):
                        return Tag(tag, id=alternate_spelling["id"], alias=True)
                    return Tag(tag)

        print(f"[INFO] Failed to find tag for query '{t}'...")
        return None

    @classmethod
    def reload(cls):
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}{CONST_DIRLIM}tags.json",
            "r",
            encoding="utf-8",
        ) as file:
            cls.tags = json.load(file)

        for tag in cls.tags:
            for spelling in tag["alternateSpellings"]:
                spelling["regex"] = re.compile(
                    r"^(" + spelling["regex"] + ")$", re.IGNORECASE
                )
