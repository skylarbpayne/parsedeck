import os
from urllib.parse import urlparse

import requests
import typer

from parsedeck.deck import export_to_anki, parse_deck


def get_content(filepath: str) -> str:
    with open(filepath, encoding="utf-8") as f:
        return f.read()


def get_url_content(url: str) -> str:
    response = requests.get(url)  # noqa: S113
    response.raise_for_status()
    return response.text


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
def combine_content_from_sources(input_sources: list[str]) -> str:
    combined_content = ""
    for source in input_sources:
        if os.path.isdir(source):
            for file in os.listdir(source):
                combined_content += get_content(os.path.join(source, file)) + "\n\n"
        elif os.path.isfile(source):
            content = get_content(source)
        elif is_valid_url(source):
            content = get_url_content(source)
        else:
            raise InvalidInputSource(source)
        combined_content += content + "\n\n"  # Add some separation between contents
    return combined_content.strip()


def main(output_file_path: str, deck_name: str, input_sources: list[str]):
    combined_content = combine_content_from_sources(input_sources)

    deck = parse_deck(combined_content.strip())
    export_to_anki(deck, deck_name, output_file_path)


if __name__ == "__main__":
    typer.run(main)
