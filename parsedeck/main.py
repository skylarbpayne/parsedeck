import os
from pathlib import Path
from urllib.parse import urlparse

import requests
import typer

from parsedeck.deck import export_to_anki, parse_deck


def get_content(filepath: str) -> str:
    with open(filepath, encoding="utf-8") as f:
        return f.read()


def get_url_content(url: str, download_dir: Path) -> str:
    response = requests.get(url)  # noqa: S113
    response.raise_for_status()
    content = response.text

    # Save the content to a local file
    parsed_url = urlparse(url)
    filename = parsed_url.path.split("/")[-1] or f"{parsed_url.netloc}_index.html"
    filepath = download_dir / filename

    # Ensure unique filename
    counter = 1
    while filepath.exists():
        name, ext = os.path.splitext(filename)
        filepath = download_dir / f"{name}_{counter}{ext}"
        counter += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


class InvalidInputSource(ValueError):
    def __init__(self, source: str):
        super().__init__(f"Invalid input source: {source}")


# TODO: support for PDF
# TODO: support for video?
def combine_content_from_sources(input_sources: list[str], download_dir: Path) -> list[str]:
    contents = []
    for source in input_sources:
        if os.path.isdir(source):
            for file in os.listdir(source):
                contents.append(get_content(os.path.join(source, file)))
        elif os.path.isfile(source):
            content = get_content(source)
        elif is_valid_url(source):
            content = get_url_content(source, download_dir)
        else:
            raise InvalidInputSource(source)
        contents.append(content)  # Add some separation between contents
    return contents


def main(output_file_path: str, deck_name: str, input_sources: list[str]):
    # Create a directory for downloaded content
    download_dir = Path("downloaded_content")
    download_dir.mkdir(exist_ok=True)

    contents = combine_content_from_sources(input_sources, download_dir)

    # Save the combined content to a file
    # with open("combined_content.txt", "w", encoding="utf-8") as f:
    #     f.write(combined_content)

    deck = parse_deck(contents)
    export_to_anki(deck, deck_name, output_file_path)


if __name__ == "__main__":
    typer.run(main)
