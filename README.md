# parsedeck

[![Release](https://img.shields.io/github/v/release/skylarbpayne/parsedeck)](https://img.shields.io/github/v/release/skylarbpayne/parsedeck)
[![Build status](https://img.shields.io/github/actions/workflow/status/skylarbpayne/parsedeck/main.yml?branch=main)](https://github.com/skylarbpayne/parsedeck/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/skylarbpayne/parsedeck/branch/main/graph/badge.svg)](https://codecov.io/gh/skylarbpayne/parsedeck)
[![Commit activity](https://img.shields.io/github/commit-activity/m/skylarbpayne/parsedeck)](https://img.shields.io/github/commit-activity/m/skylarbpayne/parsedeck)
[![License](https://img.shields.io/github/license/skylarbpayne/parsedeck)](https://img.shields.io/github/license/skylarbpayne/parsedeck)

A tool for creating Anki flashcard decks from a variety of content sources.

- **Github repository**: <https://github.com/skylarbpayne/parsedeck/>
- **Documentation** <https://skylarbpayne.github.io/parsedeck/>

## Getting Started

This project uses uv for environment/dependency management. Run:

```bash
uv run parsedeck/main.py {OUTPUT_FILE_PATH} {DECK_NAME} {INPUT_URLS}
```

to create an Anki deck from a list of URLs. This can then be imported into Anki.

## Roadmap

1. Support for broader content types (PDFs, etc.)
2. Support for different flashcard formats (Quizlet, etc.)
3. Support for total content longer than provider token limits (e.g. via RAG)
4. Logging / metrics with logfire

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
