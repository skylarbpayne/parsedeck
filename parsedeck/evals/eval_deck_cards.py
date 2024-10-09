import braintrust

from parsedeck.deck import make_card, make_deck_plan
from parsedeck.evals.dataset_urls import DATASET
from parsedeck.main import get_url_content


def run_evaluation(dataset: list[braintrust.EvalCase]):
    experiment = braintrust.init(project="FlashCardGenDeckCards")  # Replace with your project name

    for data in dataset:
        with experiment.start_span(name="generate_deck_cards") as span:
            x = data["input"]
            content = get_url_content(x)
            deck_plan = make_deck_plan(content)
            cards = [make_card(content, card_description) for card_description in deck_plan.cards_to_create]

            metadata = {
                "url": x,
                "plan": deck_plan,
                "content_length": len(content),
                "num_cards": len(cards),
                "num_planned_cards": len(deck_plan.cards_to_create),
            }

            span.log(
                input=content,
                output=cards,
                # scores={
                #     'completeness': completeness,
                #     # scope,
                # },
                metadata=metadata,  # The metadata dictionary
            )

    summary = experiment.summarize()
    print(summary)
    return summary


if __name__ == "__main__":
    run_evaluation(DATASET)
