import json
import requests


class MangadexFetcher:
    content = []
    regions = {"ja": "jp", "ko": "kr"}
    statuses = {
        "unknown": 0,
        "ongoing": 1,
        "completed": 2,
        "licensed": 3,
        "publishing finished": 4,
        "cancelled": 5,
        "on hiatus": 6,
    }

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

    def parse(self, parser):
        # Take in a function or a path and return the value
        pass

    def add_content(self, type):
        self.content.append(type)

    def build_metadata(self):
        # data = {
        #     "origin": self.parse(),
        #     "origin id": self.parse(),
        #     "series": self.parse(),
        #     "title": 0,
        #     "romanized title": self.parse(),
        #     "en title": self.parse(),
        #     "native title": self.parse(),
        #     "author": self.parse(),
        #     "artist": self.parse(),
        #     "publisher": self.parse(),
        #     "group": self.parse(),
        #     "locality": self.parse(),
        #     "en description": self.parse(),
        #     "print language": "en",
        #     "original language": self.parse(),
        #     "status": self.parse(),
        #     "translation type": 3,
        # }
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
            "origin id": [id],
            "series": None,
            "title": 0,
            "romanized title": [self.metadata["data"]["attributes"]["title"]["en"]],
            "en title": [],
            "native title": [],
            "author": creators["author"],
            "artist": creators["artist"],
            "publisher": None,
            "group": None,
            "locality": region_code,
            "en description": self.metadata["data"]["attributes"]["description"]["en"],
            "print language": "en",
            "original language": region_code,
            "status": self.statuses[self.metadata["data"]["status"]],
            "translation type": 3,
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

    def build_tags():
        data = {
            "format": [],
            "content warnings": [],
            "genre": [],
            "demographic": [],
            "tags": []
        }

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
