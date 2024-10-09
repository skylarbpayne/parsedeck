import os
from pathlib import Path
from urllib.parse import urlparse

import requests
import typer

from parsedeck.deck import export_to_anki, export_to_orbit, parse_deck


def get_content(filepath: str) -> str:
    with open(filepath, encoding="utf-8") as f:
        return f.read()


def get_url_content(url: str, download_dir: Path | None = None) -> str:
    response = requests.get(url)  # noqa: S113
    response.raise_for_status()
    content = response.text

    if download_dir is not None:
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


class InvalidExportFormat(ValueError):
    def __init__(self, export_format: str):
        super().__init__(f"Invalid output format: {export_format}")


# TODO: support for PDF
# TODO: support for video?
def get_content_from_sources(input_sources: list[str], download_dir: Path) -> list[str]:
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


def main(
    output_file_path: str,
    deck_name: str,
    input_sources: list[str],
    export_format: str = "anki",
):
    # Create a directory for downloaded content
    download_dir = Path("downloaded_content")
    download_dir.mkdir(exist_ok=True)

    contents = get_content_from_sources(input_sources, download_dir)

    deck = parse_deck(contents)

    # TODO: setup an 'Exporter' interface to make this cleaner
    if export_format == "anki":
        export_to_anki(deck, deck_name, output_file_path)
    elif export_format == "orbit":
        export_to_orbit(deck, deck_name, output_file_path)
    elif export_format == "json":
        with open(output_file_path, "w") as f:
            f.write(deck.model_dump_json(indent=2))
    else:
        raise InvalidExportFormat(export_format)


if __name__ == "__main__":
    typer.run(main)
