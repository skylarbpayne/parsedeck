import braintrust

from parsedeck.deck import DeckPlanRevisions, make_deck_plan
from parsedeck.main import get_url_content


def make_deck_plan_from_url(url: str) -> DeckPlanRevisions:
    content = get_url_content(url)
    return make_deck_plan(content)


# TODO: evals for:
# 1) Content length
# 3) Quality of cards (this is feedback on the deck LATER)


def num_revisions(output: DeckPlanRevisions) -> int:
    return len(output.plan_revisions)


def num_cards(output: DeckPlanRevisions) -> int:
    return len(output.plan_revisions[-1].cards_to_create)


DATASET = [
    {
        "input": "https://www.astronomer.io/docs/learn/dags",
    }
]


def run_evaluation(dataset: list[braintrust.EvalCase]):
    experiment = braintrust.init(project="FlashCardGen")  # Replace with your project name

    for data in dataset:
        with experiment.start_span(name="plan_deck") as span:
            x = data["input"]
            content = get_url_content(x)
            deck_revisions = make_deck_plan(content)

            metadata = {
                "num_revisions": len(deck_revisions.plan_revisions),
                "final_num_cards": len(deck_revisions.plan_revisions[-1].cards_to_create),
                "content_length": len(content),
                "final_plan": deck_revisions.plan_revisions[-1].plan,
                "final_feedback": deck_revisions.plan_revisions[-1].feedback,
            }

            span.log(
                input=x,
                output=deck_revisions,
                metadata=metadata,  # The metadata dictionary
            )

    summary = experiment.summarize()
    print(summary)
    return summary


if __name__ == "__main__":
    run_evaluation(DATASET)
