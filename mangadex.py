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

    def add_content(self, type):
        self.content.append(type)

    def build_metadata(self):
        # Region/Language
        region = self.metadata["data"]["attributes"]["originalLanguage"]
        region_code = None
        if region in self.regions:
            region_code = self.regions[region]

        # Artist and Author
        creators = {"artist": [], "author": []}
        for relationship in self.metadata["data"]["relationships"]:
            if relationship["type"] in creators:
                creators[relationship["type"]].append(relationship["attributes"]["name"])
        if len(creators["artist"]) < 1:
            creators["artist"] = creators["author"]

        data = {
            "origin": self.url["domain"],
            "originID": [self.id],
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
            "status": self.metadata["data"]["attributes"]["status"],
        }

        # Native Description
        if region in self.metadata["data"]["attributes"]["description"]:
            data["description"][self.regions["region"]] = (
                self.metadata["data"]["attributes"]["description"][region],
            )

        # Titles
        for title in self.metadata["data"]["attributes"]["altTitles"]:
            for key, value in title.items():
                if key == region:
                    data["nativeTitle"].append(value)
                    break
                if key == "en":
                    data["enTitle"].append(value)
                    break
                if key == f"{region}_ro":
                    data["romanizedTitle"].append(value)
                    break
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def build_tags(self):
        tags = []
        tags_json = []
        for tag in self.metadata["data"]["attributes"]["tags"]:
            tag_actual = TagTools.find(tag["attributes"]["name"]["en"])
            if tag_actual:
                tags.append(tag_actual)
                tags_json.append(tag_actual.json())

        print(f"Found {len(tags)} tags out of {len(self.metadata["data"]["attributes"]["tags"])}.")
        print(json.dumps(tags_json, indent=2, ensure_ascii=False))

    def build_releases():
        pass

    def run(self):
        builders = {
            "meta": self.build_metadata,
            "tags": self.build_tags,
            "releases": self.build_releases
        }
        for content_type in self.content:
            builders[content_type]()
