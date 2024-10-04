```
uv run parsedeck/main.py llm_evals.apkg "LLM Evals" "https://eugeneyan.com/writing/llm-evaluators/" "https://eugeneyan.com/writing/evals/" "https://hamel.dev/blog/posts/evals/" "https://www.sh-reya.com/blog/ai-engineering-flywheel/" "https://www.jasonwei.net/blog/evals" "https://humanloop.com/blog/contrarian-guide-to-ai"

BadRequestError: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'prompt is too long: 208208 tokens > 199999 maximum'}}
```

This is a known issue because we stuff ALL the content into a single prompt. I think the best fix is to do the following:

1. Extract concepts for cards from the content -- 1 call per piece of content (or figure out how to 'intelligently' batch)
   1a. For each call, put the already discovered concepts to reduce duplicates (make it output a set?)
2. For each concept, use RAG to get the most relevant bits of content chunks and create a card (do this in parallel).
