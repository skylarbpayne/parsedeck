```
uv run parsedeck/main.py llm_evals.apkg "LLM Evals" "https://eugeneyan.com/writing/llm-evaluators/" "https://eugeneyan.com/writing/evals/" "https://hamel.dev/blog/posts/evals/" "https://www.sh-reya.com/blog/ai-engineering-flywheel/" "https://www.jasonwei.net/blog/evals"
```

Generates a deck with only 3 cards. There should be a lot more from all this content -- it's pretty rich and in depth stuff.
Might be a limit on output length?

Maybe the better thing to do is to have separate prompts for figuring out "card concepts" vs "card details".
1 prompt for figuring out the concepts
1 prompt, multiple cards for figuring out the details
