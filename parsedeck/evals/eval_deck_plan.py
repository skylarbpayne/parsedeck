import braintrust

# from autoevals import LLMClassifier
from parsedeck.deck import DeckPlan, make_deck_plan
from parsedeck.main import get_url_content


def make_deck_plan_from_url(url: str) -> DeckPlan:
    content = get_url_content(url)
    return make_deck_plan(content)


# completeness = LLMClassifier(
#     name="completeness",
#     prompt_template="Does the following list of flashcards completely cover the content of the original text? Output only one of VERY LOW, LOW, MEDIUM, HIGH, or VERY HIGH.\n\n{output.plan_revisions[-1].cards_to_create}\n\n{input}",
#     choice_scores={
#         'VERY LOW': 0.0,
#         'LOW': 0.25,
#         'MEDIUM': 0.5,
#         'HIGH': 0.75,
#         'VERY HIGH': 1.0,
#     }
# )

# scope = LLMClassifier(
#     name="scope",
#     prompt="Does the following text have any typos or grammatical errors? {content}",
# )

URLS = [
    "https://www.astronomer.io/docs/learn/dags",
    "https://mirascope.com/docs/WHY/",
    "https://aftercompsci.com/2024/10/05/work-steroids-ai-tools-and-models/",
    "https://seattledataguy.substack.com/p/back-to-the-basics-with-sql-understanding",
    "https://seattledataguy.substack.com/p/from-basics-to-challenges-a-data",
]

DATASET = [{"input": url} for url in URLS]


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
