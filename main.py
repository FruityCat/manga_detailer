import argparse
import os
import platform
import re
import nanoid
import json

from mangadex import MangadexFetcher

# from jsonschema import validate, ValidationError


CONST_URL_PATTERN = re.compile(
    r"^(?P<scheme>https?)://" r"(?P<domain>[^/]+)" r"(?P<path>/[^?]*)?"
)


DETAILS_TEMPLATE = {}


PARSER = argparse.ArgumentParser(
    prog="Manga Detailer",
    description="Generate details.json for use with Nyarchive.",
    epilog="",
)


def choose_fetcher(domain):
    if domain == "mangadex.org":
        return MangadexFetcher()
    if domain == "anilist.co":
        pass
    if domain == "anime-planet.com":
        pass
    if domain == "mangaupdates.com":
        pass


def get_url_segments(url):
    match = CONST_URL_PATTERN.match(url)
    meta_url_segments = {}
    if match:
        meta_url_segments = match.groupdict()
        return meta_url_segments
    return None


def fetch(url, type):
    segments = get_url_segments(url)
    if not segments:
        print(f"Failed to return segments for metadata URL: {url}. Skipping.")
        return
    print(
        f"Successfully found segment fetcher for {segments["domain"]}{segments["path"]}. Scraping..."
    )

    fetcher = choose_fetcher(segments["domain"], segments)
    return fetcher.get_details(type)


def main():
    global PARSER
    global DETAILS_TEMPLATE
    details = {}
    previous_details = {}

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
        dest="force refresh",
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

    # This feels pretty gross...
    # Two options, we recreate the SourceFetcher object every time for meta, tags, and releases.
    # or... we somehow add the ones needed to a list with the needed information stored and only
    # create the fetcher object once.
    # Just recreating it everytime is easier at the moment.
    # could have like... metabuilder, tags builder, and releases builder. Somehow have meta and
    # tag builder point to the same object and add the flag via a setter. (Yes... do this.)
    if args.meta:
        details.append(fetch(args.meta[0], "meta"))
    if args.tags:
        details.append(fetch(args.tags[0], "tags"))
    if args.releases:
        details.append(fetch(args.releases[0], "releases"))

    if os.path.exists(f"{directory}/details.json"):
        with open("details.json", "r") as details:
            previous_details = json.load(details)

    if (
        not args["force refresh"][0]
        and "id" in previous_details  # noqa: W503
        and previous_details["id"] != ""  # noqa: W503
    ):
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
