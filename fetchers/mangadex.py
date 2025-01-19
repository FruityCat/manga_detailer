import json
import re
import cutlet
import requests

from tagging.tag_tools import TagTools
from language_tools.JPTools import JPTools


class MangadexFetcher:
    content = []
    regions = {"ja": "jp", "ko": "kr"}
    types = ["genre", "theme", "content warning", "demographic", "format"]

    url = {}
    metadata = {}
    details = {}

    def __init__(self, url) -> None:
        self.url = url
        path = url["path"].replace("/title/", "")
        self.id = path[: path.find("/")]

        api_url = f"https://api.mangadex.org/manga/{self.id}?includes[]=artist&includes[]=author&includes[]=cover_art"
        request = requests.get(api_url)
        if request.status_code != 200:
            print(
                f"Failed to fetch response from {api_url}. Skipping metadata scrapping... Response code: {request.status_code}"
            )
            return None

        response = request.content
        request.close()

        self.metadata = json.loads(response)

    def add_content(self, type) -> None:
        self.content.append(type)

    def __fetch_titles(self) -> dict:
        titles = {}
        titles["preferred"] = [
            "en",
            "ro_jp",
            "jp",
            "kr",
            "zh-cn",
        ]  # This is the order to choose preferred title in
        for title in self.metadata["data"]["attributes"]["altTitles"]:  # A
            # Flattening out JSON object
            for key, value in title.items():  # B
                if key in titles:
                    if key == "ro_ja":
                        value = JPTools.remove_macrons(value)
                    titles[key].append(value)
                    break  # B

        # If JP, we need some additional checks for Romaji. If not we can leave now.
        if self.metadata["data"]["attributes"]["originalLanguage"] != "ja":
            return titles

        # If there is an alternate ro_jp title and it matches the preferred title,
        # we know the preferred title is ro_jp.
        # This is unlikely because alternate titles use macrons and preferred title
        # as romanised uses vowel pairs.
        if "en" in self.metadata["data"]["attributes"]["title"] and "ro_jp" in titles:
            for ro_jp in titles["ro_jp"]:
                ro_jp_no_macrons = ro_jp
                if JPTools.is_macronised(ro_jp):
                    ro_jp_no_macrons = JPTools.remove_macrons(ro_jp)

                if ro_jp_no_macrons != self.metadata["data"]["attributes"]["title"]["en"]:
                    continue

                titles["ro_jp"].remove("ro_jp")
                titles["ro_jp"].insert(0, ro_jp)

        # If you're here, assume that ro_jp doesn't exist in alternate titles
        # and that we don't know whether title is "en": "ro_jp" or "en": "en"

        # If no native language exists in alternates, we assume it's English because
        # it doesn't make sense to only have the ro_jp version for a manga made in Japan.
        preferred_title = self.metadata["data"]["attributes"]["title"]["en"]
        if "jp" not in titles:
            if "en" not in titles:
                titles["en"] = [preferred_title]
                return titles

            if preferred_title not in titles["en"]:
                titles["en"].insert(0, preferred_title)
                return titles

        # Check with Cutlet
        katsu = cutlet.Cutlet()
        katsu_fr = cutlet.Cutlet()
        katsu_fr.use_foreign_spelling = False

        for jp in titles["jp"]:
            ro_jp = katsu.romaji(jp)
            fr_ro_jp = katsu_fr.romaji(jp)
            reg = JPTools.foregin_word_regex(ro_jp, fr_ro_jp)

            if bool(re.match(reg, preferred_title)):
                preferred_title_macronised = preferred_title
                if not JPTools.is_macronised(preferred_title):
                    preferred_title_macronised = JPTools.add_macrons(preferred_title)

                if "ro_jp" not in titles:
                    titles["ro_jp"] = [preferred_title_macronised]
                    return titles

                if preferred_title_macronised in titles["ro_jp"]:
                    titles["ro_jp"].remove(preferred_title_macronised)
                # At this point preferred_title_macronised should be in the lsit already, we just need to make
                # sure that it's the primary one.
                titles["ro_jp"].insert(0, preferred_title_macronised)
                return titles

        # At this point the title can be dropped with a warning.
        print("[INFO] Primary title language could not be determined. Added as English")
        if "en" not in titles:
            titles["en"] = [preferred_title]
            return titles

        if preferred_title in titles["en"]:
            titles["en"].remove(preferred_title)
        titles["en"].insert(0, preferred_title)

        return titles

    def __build_metadata(self) -> None:
        # Region/Language
        region = self.metadata["data"]["attributes"]["originalLanguage"]
        region_code = None
        if region in self.regions:
            region_code = self.regions[region]

        # Artist and Author
        creators = {"artist": [], "author": []}
        for relationship in self.metadata["data"]["relationships"]:
            if relationship["type"] in creators:
                creators[relationship["type"]].append(
                    relationship["attributes"]["name"]
                )
        if len(creators["artist"]) < 1:
            creators["artist"] = creators["author"]

        data = {
            "origin": self.url["domain"],
            "originID": [self.id],
            "series": None,
            "titles": self.__fetch_titles(),
            "author": creators["author"],
            "artist": creators["artist"],
            "publisher": None,
            "group": None,
            "locality": region_code,
            "description": {
                "en": self.metadata["data"]["attributes"]["description"]["en"]
            },
            "printLanguage": "en",
            "originalLanguage": region_code,
            "status": self.metadata["data"]["attributes"]["status"],
        }

        # Native Description
        if region in self.metadata["data"]["attributes"]["description"]:
            data["description"][self.regions["region"]] = (
                self.metadata["data"]["attributes"]["description"][region],
            )

        print(json.dumps(data, indent=2, ensure_ascii=False))

    def __build_tags(self) -> None:
        tags = []
        tags_json = []
        for tag in self.metadata["data"]["attributes"]["tags"]:
            tag_actual = TagTools.find(tag["attributes"]["name"]["en"])
            if tag_actual:
                tags.append(tag_actual)
                tags_json.append(tag_actual.json())

        print(
            f"Found {len(tags)} tags out of {len(self.metadata["data"]["attributes"]["tags"])}."
        )
        print(json.dumps(tags_json, indent=2, ensure_ascii=False))

    def __build_releases():
        pass

    def run(self):
        builders = {
            "meta": self.__build_metadata,
            "tags": self.__build_tags,
            "releases": self.__build_releases,
        }
        for content_type in self.content:
            builders[content_type]()
