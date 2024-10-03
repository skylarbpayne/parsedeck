import random

import genanki
from mirascope.core import anthropic, prompt_template
from pydantic import BaseModel, Field


class Card(BaseModel):
    front: str = Field(..., description="The front of the card")
    back: str = Field(..., description="The back of the card")
    sources: list[str] = Field(..., description="The sources for the extracted front and back of the card")
    reasoning: str = Field(..., description="The reasoning for the answer")


class Deck(BaseModel):
    plan: str = Field(..., description="The plan for the structure and organization of the deck")
    cards_to_create: list[str] = Field(
        ..., description="A short description of which cards to create; an extension of the plan"
    )
    cards: list[Card] = Field(..., description="The list of flashcards")


@anthropic.call(
    model="claude-3-5-sonnet-20240620",
    response_model=Deck,
    json_mode=True,
)
@prompt_template(
    """
    You are an expert at parsing content into flashcards. You know how to extract the most relevant information from a given text and format it into a simple front/back flashcard.
    You create flashcards ranging from easy to hard, and you always include the sources you used to create the flashcards to prevent information from being made up.
    Some of your flashcards will be conceptual, and others will be Q&A style.

    Create flashcards from the following content:
    {content}
    """
)
def parse_deck(content: str) -> Deck: ...


def export_to_anki(deck: Deck, deck_name: str, output_file: str = "output.apkg"):
    # Create a unique model ID
    model_id = random.randrange(1 << 30, 1 << 31)  # noqa: S311

    # Define the Anki model
    model = genanki.Model(
        model_id,
        "Parsedeck Model",
        fields=[
            {"name": "Front"},
            {"name": "Back"},
            {"name": "Sources"},
            {"name": "Reasoning"},
        ],
        templates=[
            {
                "name": "Card",
                "qfmt": "{{Front}}",
                "afmt": """
                    {{FrontSide}}
                    <hr id="answer">
                    {{Back}}
                    <hr>
                    <small>Sources: {{Sources}}</small>
                    <br>
                    <small>Reasoning: {{Reasoning}}</small>
                """,
            },
        ],
    )

    # Create a unique deck ID
    deck_id = random.randrange(1 << 30, 1 << 31)  # noqa: S311

    # Create the Anki deck
    anki_deck = genanki.Deck(deck_id, deck_name)

    # Add notes to the deck
    for card in deck.cards:
        note = genanki.Note(model=model, fields=[card.front, card.back, ", ".join(card.sources), card.reasoning])
        anki_deck.add_note(note)

    # Create and write the package
    genanki.Package(anki_deck).write_to_file(output_file)
