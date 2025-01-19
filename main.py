import argparse
import os
import platform
import re
import nanoid
import json

from fetchers.mangadex import MangadexFetcher
from tagging.tag_tools import TagTools

# from jsonschema import validate, ValidationError


# See get_url_segments(url) -> dict
CONST_URL_PATTERN = re.compile(
    r"^(?P<scheme>https?)://" r"(?P<domain>[^/]+)" r"(?P<path>/[^?]*)?"
)


DETAILS_TEMPLATE = {}


PARSER = argparse.ArgumentParser(
    prog="Manga Detailer",
    description="Generate details.json for use with Nyarchive.",
    epilog="",
)


def choose_fetcher(domain, url_segments):
    """
    I want a switch case please... ;~;
    """
    if domain == "mangadex.org":
        return MangadexFetcher(url_segments)
    if domain == "anilist.co":
        pass
    if domain == "anime-planet.com":
        pass
    if domain == "mangaupdates.com":
        pass


def get_url_segments(url) -> dict:
    """
    Splits URL into scheme (protocol), domain, path
    EG: {
        "scheme": "https",
        "domain", "mangadex.org",
        "path": "/manga/ABCEXAMPLEMANGA123"
    }
    """
    match = CONST_URL_PATTERN.match(url)
    meta_url_segments = {}
    if match:
        meta_url_segments = match.groupdict()
        return meta_url_segments
    return None


def update_fetchers(url, fetchers, type) -> dict:
    """
    We want to keep a dict of {domain: fetcher} where each fetcher can have a content type
    that it fetches.

    When we add a fetcher, if the domain exists, just add the content type to its fetcher
    but if not, add fetcher to domain and set content type.
    """
    segments = get_url_segments(url)
    if not segments:
        print(f"Failed to return segments for metadata URL: {url}. Skipping.")
        return fetchers
    print(
        f"Successfully found segment fetcher for {segments["domain"]}{segments["path"]}. Scraping..."
    )

    if segments["domain"] not in fetchers:
        fetchers[segments["domain"]] = choose_fetcher(segments["domain"], segments)

    fetchers[segments["domain"]].add_content(type)
    return fetchers


def main():
    TagTools.reload()
    global PARSER
    global DETAILS_TEMPLATE
    details = {}
    previous_details = {}

    fetchers = {}

    PARSER.add_argument(
        "-d",
        "--directory",
        dest="directory",
        nargs=1,
        default=f"{os.getcwd()}",
        help="Takes the root directory of the content you're trying to detail.",
    )  # noqa: E501
    PARSER.add_argument(
        "-t",
        "--tags",
        dest="tags",
        nargs=1,
        default=None,
        help="Source to grab tags from: supported visible on GitHub.",
    )  # noqa: E501
    PARSER.add_argument(
        "-m",
        "--meta",
        dest="meta",
        nargs=1,
        default=None,
        help="Source to grab metadata (author, title, etc) from.",
    )  # noqa: E501
    PARSER.add_argument(
        "-r",
        "--releases",
        dest="releases",
        nargs=1,
        default=None,
        help="Source to grab volume and chapter info from.",
    )  # noqa: E501
    PARSER.add_argument(
        "-o",
        "--origin",
        dest="origin",
        nargs=1,
        default=None,
        help="Override the origin so it doesn't set to the one grabbed from metadata.",
    )  # noqa: E501
    PARSER.add_argument(
        "-f",
        "--force-refresh",
        dest="force_refresh",
        default=False,
        help="Whether to force refresh ID.",
        action=argparse.BooleanOptionalAction,
    )  # noqa: E501
    args = PARSER.parse_args()

    directory = args.directory
    software_dir = os.path.dirname(os.path.abspath(__file__))
    dirlim = "/"
    if platform.system() == "Windows":
        dirlim = "\\"

    if directory.startswith("./") or directory.startswith(".\\"):
        directory = f"{os.getcwd()}{dirlim}{directory[2:]}"

    # Build the fetcher army!!! c:<
    if args.meta:
        fetchers = update_fetchers(args.meta[0], fetchers, "meta")
    if args.tags:
        fetchers = update_fetchers(args.tags[0], fetchers, "tags")
    if args.releases:
        fetchers = update_fetchers(args.releases[0], fetchers, "releases")

    if os.path.exists(f"{directory}/details.json"):
        with open("details.json", "r") as details:
            previous_details = json.load(details)

    if (
        not args.force_refresh
        and "id" in previous_details  # noqa: W503
        and previous_details["id"] != ""  # noqa: W503
    ):
        details["id"] = previous_details["id"]
    else:
        details["id"] = nanoid.generate()

    for domain, fetcher in fetchers.items():
        new_details = fetcher.run()
        print(new_details)

    # with open(f"{software_dir}/details_template.json", "r") as template:
    #     DETAILS_TEMPLATE = json.load(template)

    # try:
    #     with (open(f"{software_dir}/schema.json", "r")) as file:
    #         schema = json.load(file)
    #         validate(instance=details, schema=schema)
    # except ValidationError:
    #     print("Error validating against schema for details.json. Write cancelled.")
    #     print(f"{ValidationError}")
    #     return

    # with open(f"{directory}/details.json", "w") as details:
    #     print("Writing to details.json not implemented yet.")


if __name__ == "__main__":
    main()
