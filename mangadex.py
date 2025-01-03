import json
import requests


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
            tags.append(TagTools.find(tag["attributes"]["name"]["en"]))

    def build_releases():
        pass

    def get_details(self):
        if "meta" in self.content:
            self.build_metadata()
        if "tags" in self.content:
            self.build_tags()
        if "releases" in self.content:
            self.build_releases()

        return self.details
