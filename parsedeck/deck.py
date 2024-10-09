import random
from pathlib import Path

import genanki
from mirascope.core import openai, prompt_template
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential


class Card(BaseModel):
    front: str = Field(..., description="The front of the card")
    back: str = Field(..., description="The back of the card")
    sources: list[str] = Field(..., description="The sources for the extracted front and back of the card")
    reasoning: str = Field(..., description="The reasoning for the answer")


class Deck(BaseModel):
    cards: list[Card] = Field(..., description="The list of flashcards")


class DeckPlan(BaseModel):
    reasoning: str = Field(..., description="The reasoning for the plan")
    plan: str = Field(..., description="The plan for the structure and organization of the deck")
    cards_to_create: list[str] = Field(
        ..., description="A short description of which cards to create; an extension of the plan"
    )


# TODO: make the model configurable
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=60, max=120),
)
@openai.call(
    model="gpt-4o-mini",
    response_model=DeckPlan,
    json_mode=True,
)
@prompt_template(
    """
    You are an expert at parsing content into flashcards. You know how to extract the most relevant information from a given text and format it into a simple front/back flashcard.
    You create flashcards ranging from easy to hard, and you always include the sources you used to create the flashcards to prevent information from being made up.
    Some of your flashcards will be conceptual, and others will be Q&A style.

    You always spend a few sentences thinking about the best way to structure the deck. Your planned decks should:

    - Be Accurate
    - Be Complete and Comprehensive
    - Have a Logical Structure
    - Have a good variety of flashcards

    Create a plan for the deck from the following content.
    {content}
    """
)
def make_deck_plan(content: str) -> DeckPlan: ...


# TODO: make the model configurable
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=20, max=60),
)
@openai.call(
    model="gpt-4o-mini",
    response_model=Card,
    json_mode=True,
)
@prompt_template(
    """
    You are an expert at parsing content into flashcards. You know how to extract the most relevant information from a given text and format it into a simple front/back flashcard.
    You create flashcards ranging from easy to hard, and you always include the sources you used to create the flashcards to prevent information from being made up.
    Some of your flashcards will be conceptual, and others will be Q&A style.

    Create a single flashcard from the following prompt and content.

    # Prompt
    {card_description}
    # Content
    {content}
    """
)
def make_card(content: str, card_description: DeckPlan) -> Card: ...


# Rate limit issues??
def parse_deck(contents: list[str]) -> Deck:
    cards = []
    for content in contents:
        plan = make_deck_plan(content)
        cards.extend([
            make_card(content, card_description) for card_description in plan.plan_revisions[-1].cards_to_create
        ])
    return Deck(cards=cards)


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


# ... existing code ...


def export_to_orbit(deck: Deck, deck_name: str, output_file: str = "output.html"):
    # Create the HTML content
    html_content = f"""
<html>
  <head>
    <title>{deck_name}</title>
    <script type="module" src="https://js.withorbit.com/orbit-web-component.js"></script>
  </head>
  <body>
    <h1>{deck_name}</h1>
    <orbit-reviewarea color="brown">
"""

    # Add each card as an orbit-prompt
    for card in deck.cards:
        html_content += f"""
      <orbit-prompt
        question="{card.front}"
        answer="{card.back}"
      ></orbit-prompt>
"""

    # Close the HTML tags
    html_content += """
    </orbit-reviewarea>
  </body>
</html>
"""

    # Write the HTML content to the output file
    output_path = Path(output_file)
    output_path.write_text(html_content, encoding="utf-8")
