#!/usr/bin/env python3

import datetime
import argparse
import sys
import os
import requests

LANGUAGE_NAMES = {
    "en": {"subtag": "en", "english": "English"},
    "fr": {"subtag": "fr", "english": "French"},
    "de": {"subtag": "de", "english": "German"},
    # ajoute d'autres si besoin
}

USER_AGENT = "ArchWikiDownloader/1.0 (+https://archlinux.org)"


def fetch_page(title, lang="en"):
    url = f"https://{lang}.wiki.archlinux.org/api.php"
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        "redirects": True,
    }
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    return r.json()["parse"]["text"]["*"]


def save_page(title, html, output_dir, safe_filename=False):
    filename = title if not safe_filename else title.replace("/", "_").encode("ascii", "ignore").decode()
    path = os.path.join(output_dir, f"{filename}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def list_languages():
    for lang in LANGUAGE_NAMES.values():
        print(lang['subtag'], lang['english'])


def main():
    parser = argparse.ArgumentParser(description="Download Arch Wiki pages for offline viewing.")
    parser.add_argument("--output-directory", required=True, help="Where to store downloaded pages")
    parser.add_argument("--force", action="store_true", help="Force re-download")
    parser.add_argument("--clean", action="store_true", help="Clean unknown files in output directory")
    parser.add_argument("--safe-filenames", action="store_true", help="ASCII-only filenames")
    parser.add_argument("--langs", nargs="+", help="Languages to download (e.g. en fr)")
    parser.add_argument("--list-langs", action="store_true", help="List supported languages")
    args = parser.parse_args()

    if args.list_langs:
        list_languages()
        sys.exit(0)

    langs = args.langs or ["en"]
    output_dir = args.output_directory
    os.makedirs(output_dir, exist_ok=True)

    titles = ["Pacman", "Installation guide", "Xorg", "Systemd"]  # exemple

    for lang in langs:
        for title in titles:
            print(f"Downloading '{title}' [{lang}]...")
            try:
                html = fetch_page(title, lang)
                save_page(title, html, output_dir, args.safe_filenames)
            except Exception as e:
                print(f"Error fetching {title} [{lang}]: {e}")

    if args.clean:
        known_files = {f"{t}.html" for t in titles}
        for f in os.listdir(output_dir):
            if f not in known_files:
                os.remove(os.path.join(output_dir, f))


if __name__ == "__main__":
    main()
