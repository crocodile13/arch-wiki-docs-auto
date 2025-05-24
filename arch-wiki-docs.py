#!/usr/bin/env python3

import argparse
import datetime
import sys

from simplemediawiki import build_user_agent
import ArchWiki
from ArchWiki.ArchWiki import language_names


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download pages from Arch Wiki and optimize them for offline browsing"
    )
    parser.add_argument(
        "--output-directory", type=str, required=True,
        help="Path where the downloaded pages should be stored."
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Ignore timestamp, always download the page from the wiki."
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Clean the output directory after downloading. "
             "Warning: unknown files found in the directory will be deleted!"
    )
    parser.add_argument(
        "--safe-filenames", action="store_true",
        help="Use ASCII-only filenames instead of Unicode."
    )
    parser.add_argument(
        "--langs", type=str, nargs='+',
        help="Download only pages of specified languages."
    )
    parser.add_argument(
        "--list-langs", action="store_true",
        help="List supported languages and exit."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.list_langs:
        for lang in language_names.values():
            print(f"{lang['subtag']}: {lang['english']}")
        sys.exit(0)

    epoch = datetime.datetime.utcnow() if args.force else datetime.datetime(2016, 3, 3, 18, 0, 0)

    user_agent = build_user_agent(__file__, ArchWiki.__version__, ArchWiki.__url__)
    aw = ArchWiki.ArchWiki(user_agent=user_agent, safe_filenames=args.safe_filenames, langs=args.langs)
    optimizer = ArchWiki.Optimizer(aw, args.output_directory)

    downloader = ArchWiki.Downloader(aw, args.output_directory, epoch, optimizer=optimizer)
    downloader.download_css()
    aw.print_namespaces()

    for ns in ["0", "4", "12", "14"]:
        downloader.process_namespace(ns)

    downloader.download_images()

    if args.clean:
        downloader.clean_output_directory()


if __name__ == "__main__":
    main()
