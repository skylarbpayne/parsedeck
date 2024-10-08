import braintrust

from parsedeck.deck import make_deck_plan
from parsedeck.evals.dataset_urls import DATASET
from parsedeck.main import get_url_content


def run_evaluation(dataset: list[braintrust.EvalCase]):
    experiment = braintrust.init(project="FlashCardGen")  # Replace with your project name

    for data in dataset:
        with experiment.start_span(name="plan_deck") as span:
            x = data["input"]
            content = get_url_content(x)
            deck_plan = make_deck_plan(content)

            metadata = {
                "url": x,
                # "num_revisions": len(deck_plan.plan_revisions),
                "final_num_cards": len(deck_plan.cards_to_create),
                "content_length": len(content),
                "final_plan": deck_plan.plan,
                # "final_feedback": deck_revisions.plan_revisions[-1].feedback,
                # "num_cards": [len(revision.cards_to_create) for revision in deck_revisions.plan_revisions],
            }

            span.log(
                input=content,
                output=deck_plan,
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
