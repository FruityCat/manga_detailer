import argparse
import os
import platform
import random
import shutil
import sys
import time

import requests
import json
import re


CONST_URL_PATTERN = re.compile(r'^(?P<scheme>https?)://' r'(?P<domain>[^/]+)' r'(?P<path>/[^?]*)?')


DETAILS_TEMPLATE = {}
DETAILS = {}


PARSER = argparse.ArgumentParser(
    prog="Manga Detailer",
    description="Generate details.json for use with Nyarchive.",
    epilog=""
)


def fetch_mangadex(segments, requested):
    # https://mangadex.org/title/<ID>/mousou-sensei
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
    print(f"Successfully found segment fetcher for {segments["domain"]}{segments["path"]}. Scrapping...")

    fetch = choose_fetcher(segments["domain"])
    fetch(segments, "meta")


def main():
    global PARSER
    global DETAILS_TEMPLATE
    global DETAILS

    PARSER.add_argument("-d", "--directory", dest="directory", nargs=1, default=f"{os.getcwd()}", help="Takes the root directory of the content you're trying to detail.")  # noqa: E501
    PARSER.add_argument("-t", "--tags", dest="tags", nargs=1, default=None, help="Source to grab tags from: supported visible on GitHub.")  # noqa: E501
    PARSER.add_argument("-m", "--meta", dest="meta", nargs=1, default=None, help="Source to grab metadata (author, title, etc) from.")  # noqa: E501
    PARSER.add_argument("-v", "--volume", dest="volume", nargs=1, default=None, help="Source to grab volume and chapter info from.")  # noqa: E501
    args = PARSER.parse_args()

    directory = args.directory
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

    with open("details_template.json", "r") as template:
        DETAILS_TEMPLATE = json.load(template)

    with open("details.json", "w") as details:
        pass


if __name__ == "__main__":
    main()
