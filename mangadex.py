import json
import requests

from tag_tools import TagTools


class MangadexFetcher:
    content = []
    regions = {"ja": "jp", "ko": "kr"}
    types = ["genre", "theme", "content warning", "demographic", "format"]

    url = {}
    metadata = {}
    details = {}

    def __init__(self, url):
        self.url = url
        path = url["path"].replace("/title/", "")
        id = path[: path.find("/")]

        api_url = f"https://api.mangadex.org/manga/{id}?includes[]=artist&includes[]=author&includes[]=cover_art"
        request = requests.get(api_url)
        if request.status_code != 200:
            print(
                f"Failed to fetch response from {api_url}. Skipping metadata scrapping... Response code: {request.status_code}"
            )
            return None

        response = request.content
        request.close()

        self.metadata = json.loads(response)

    def add_content(self, type):
        self.content.append(type)

    def build_metadata(self):
        # Region/Language
        region = self.metadata["data"]["attributes"]["originalLanguage"]
        if region in self.regions:
            region_code = self.regions[region]

        # Artist and Author
        creators = {"artist": [], "author": []}
        for relationship in self.metadata["data"]["relationships"]:
            creators[relationship["type"]].append(relationship["attributes"]["name"])
        if len(creators["artist"]) < 1:
            creators["artist"] = creators["author"]

        data = {
            "origin": self.url["domain"],
            "originID": [id],
            "series": None,
            "title": 0,
            "romanizedTitle": [self.metadata["data"]["attributes"]["title"]["en"]],
            "enTitle": [],
            "nativeTitle": [],
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
            "status": self.metadata["data"]["status"],
        }

        # Native Description
        if region in self.metadata["data"]["attributes"]["description"]:
            data["native description"] = (
                self.metadata["data"]["attributes"]["description"][region],
            )

        # Titles
        for title in self.metadata["data"]["attributes"]["altTitles"]:
            for key, value in title.items():
                if key == region:
                    data["native title"].append(value)
                    break
                if key == "en":
                    data["en title"].append(value)
                    break
                if key == f"{region}_ro":
                    data["romanized title"].append(value)
                    break

    def build_tags(self):
        tags = []
        for tag in self.metadata["data"]["attributes"]["tags"]:
            tag_actual = TagTools.find(tag["attributes"]["name"]["en"])
            if tag_actual:
                tags.append(tag_actual)
        print(f"Found {len(tags)} tags out of {len(self.metadata["data"]["attributes"]["tags"])}.")

    def build_releases():
        pass

    def run(self):
        builders = {
            "meta": self.build_meta,
            "tags": self.build_tags,
            "releases": self.build_releases
        }
        for content_type in self.content:
            builders[content_type]()
