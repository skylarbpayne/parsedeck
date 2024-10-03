import requests
import typer

from parsedeck.deck import export_to_anki, parse_deck


def get_content(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def main(output_file_path: str, deck_name: str, input_urls: list[str]):
    combined_content = ""
    for url in input_urls:
        response = requests.get(url)  # noqa: S113
        combined_content += response.text + "\n\n"  # Add some separation between contents

    deck = parse_deck(combined_content.strip())
    export_to_anki(deck, deck_name, output_file_path)


if __name__ == "__main__":
    typer.run(main)
