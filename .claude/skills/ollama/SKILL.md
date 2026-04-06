# Skill: ollama

Route a prompt directly to the local Ollama model (qwen3-coder:30b) and return the response.

## Trigger

`/ollama [prompt]`

The entire text after `/ollama` is the prompt. Examples:

- `/ollama summarize this: [paste text]`
- `/ollama what are the key differences between a boundary survey and an ALTA survey?`
- `/ollama write a python function that parses a CSV and returns a dict`

## Steps

1. Take everything after `/ollama` as the user's prompt verbatim. Do not modify, interpret, or add to it.

2. Use the Bash tool to run:
   ```
   "C:\Users\cjani\.local\bin\python3.14.exe" ".claude/lib/ollama_query.py" --prompt "<prompt>" --model "qwen3-coder:30b"
   ```
   Substitute `<prompt>` with the user's prompt. If the prompt contains quotes, escape them properly.

3. Print the response from stdout directly to the user. Do not editorialize, summarize, or wrap it — show exactly what Ollama returned.

4. If the script exits with code 1 (stderr contains an error), tell the user: "Ollama is not reachable. Make sure it's running: `ollama serve`"

## Notes

- No system prompt is set by default — the model responds as-is
- If the user wants a system prompt, they can include it in their message: `/ollama [system: You are X] [prompt]` — parse accordingly
- This skill does not save drafts, call MCP tools, or modify files unless the user explicitly asks
