import argparse
import os
import platform
import re
import requests
import nanoid
import json
# from jsonschema import validate, ValidationError


CONST_URL_PATTERN = re.compile(r'^(?P<scheme>https?)://' r'(?P<domain>[^/]+)' r'(?P<path>/[^?]*)?')


DETAILS_TEMPLATE = {}


PARSER = argparse.ArgumentParser(
    prog="Manga Detailer",
    description="Generate details.json for use with Nyarchive.",
    epilog=""
)


def fetch_mangadex(segments, requested):
    path = segments["path"].replace("/title/", "")
    id = path[:path.find("/")]

    api_url = f"https://api.mangadex.org/manga/{id}?includes[]=artist&includes[]=author&includes[]=cover_art"
    request = requests.get(api_url)
    if request.status_code != 200:
        print(f"Failed to fetch response from {api_url}. Skipping metadata scrapping... Response code: {request.status_code}")
        return None

    response = request.content
    request.close()

    response = json.loads(response)

    if requested == "meta":
        # grab metadata here
        return {}

    if requested == "tags":
        # grab tags here
        return {}

    # grab volumes/chapters here.
    return {}


def fetch_nhentai(segments, requested):
    pass


def fetch_anilist(segments, requested):
    pass


def fetch_anime_planet(segments, requested):
    pass


def fetch_mangaupdates(segments, requested):
    pass


def choose_fetcher(domain):
    fetchers = {
        "mangadex.org": fetch_mangadex,
        "nhentai.net": fetch_nhentai,
        "anilist.co": fetch_anilist,
        "anime-planet.com": fetch_anime_planet,
        "mangaupdates.com": fetch_mangaupdates
    }

    return fetchers[domain]


def get_url_segments(url):
    match = CONST_URL_PATTERN.match(url)
    meta_url_segments = {}
    if match:
        meta_url_segments = match.groupdict()
        return meta_url_segments
    return None


def meta_data(meta_url):
    segments = get_url_segments(meta_url)
    if not segments:
        print(f"Failed to return segments for metadata URL: {meta_url}. Skipping.")
        return
    print(f"Successfully found segment fetcher for {segments["domain"]}{segments["path"]}. Scraping...")

    fetch = choose_fetcher(segments["domain"])
    fetch(segments, "meta")


def main():
    global PARSER
    global DETAILS_TEMPLATE
    details = {}
    previous_details = {}

    PARSER.add_argument("-d", "--directory", dest="directory", nargs=1, default=f"{os.getcwd()}", help="Takes the root directory of the content you're trying to detail.")  # noqa: E501
    PARSER.add_argument("-t", "--tags", dest="tags", nargs=1, default=None, help="Source to grab tags from: supported visible on GitHub.")  # noqa: E501
    PARSER.add_argument("-m", "--meta", dest="meta", nargs=1, default=None, help="Source to grab metadata (author, title, etc) from.")  # noqa: E501
    PARSER.add_argument("-v", "--volume", dest="volume", nargs=1, default=None, help="Source to grab volume and chapter info from.")  # noqa: E501
    PARSER.add_argument("-R", "--force-refresh", dest="force refresh", default=False, help="Whether to force refresh ID.", action=argparse.BooleanOptionalAction)  # noqa: E501
    args = PARSER.parse_args()

    directory = args.directory
    software_dir = os.path.dirname(os.path.abspath(__file__))
    dirlim = "/"
    if platform.system() == "Windows":
        dirlim = "\\"

    if directory.startswith("./") or directory.startswith(".\\"):
        directory = f"{os.getcwd()}{dirlim}{directory[2:]}"

    if args.meta:
        meta_data(args.meta[0])
    if args.tags:
        meta_data(args.meta[0])
    if args.volume:
        meta_data(args.meta[0])

    if os.path.exists(f"{directory}/details.json"):
        with open("details.json", "r") as details:
            previous_details = json.load(details)

    if "id" in previous_details and previous_details["id"] != "":
        details["id"] = previous_details["id"]
    else:
        details["id"] = nanoid.generate()

    with open(f"{software_dir}/details_template.json", "r") as template:
        DETAILS_TEMPLATE = json.load(template)

    # try:
    #     with (open(f"{software_dir}/schema.json", "r")) as file:
    #         schema = json.load(file)
    #         validate(instance=details, schema=schema)
    # except ValidationError:
    #     print("Error validating against schema for details.json. Write cancelled.")
    #     print(f"{ValidationError}")
    #     return

    with open(f"{directory}/details.json", "w") as details:
        print("Writing to details.json not implemented yet.")


if __name__ == "__main__":
    main()
