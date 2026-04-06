# .claude/lib — Shared Utilities

Reusable scripts that skills can call via Claude's Bash tool.

---

## ollama_query.py

Calls a local [Ollama](https://ollama.com) model and prints the response to stdout. No external dependencies — pure Python stdlib.

### Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--prompt` | Yes | — | User prompt |
| `--model` | No | `qwen3-coder:30b` | Ollama model name |
| `--system` | No | (none) | System prompt |
| `--url` | No | `http://localhost:11434` | Ollama base URL |

### Basic usage

```bash
"C:\Users\cjani\.local\bin\python3.14.exe" ".claude/lib/ollama_query.py" --prompt "Summarize this paragraph: ..."
```

### With system prompt and custom model

```bash
"C:\Users\cjani\.local\bin\python3.14.exe" ".claude/lib/ollama_query.py" \
  --prompt "Draft a one-line project description." \
  --model "qwen3-coder:30b" \
  --system "You are a civil engineering assistant for Topex Inc."
```

### Capturing output in a skill

In a SKILL.md, instruct Claude to run the script via Bash and use the stdout response in the next step:

```
Use the Bash tool to run:
  "C:\Users\cjani\.local\bin\python3.14.exe" ".claude/lib/ollama_query.py" --prompt "<assembled prompt>" --system "<role>"
Then use the printed response to continue.
```

### When to use Ollama vs Claude

| Situation | Use |
|---|---|
| Large document chunking or batch summarization | Ollama (local, no token cost) |
| Code-heavy analysis (qwen3-coder is strong here) | Ollama |
| Tasks requiring MCP tools (Gmail, Calendar) | Claude |
| Client-facing drafts requiring judgment | Claude |
| Ollama server not running | Claude (fallback) |

### Exit codes

- `0` — success, response on stdout
- `1` — error (Ollama not reachable, bad model name, etc.), details on stderr

### Prerequisites

Ollama must be running locally:

```bash
ollama serve
ollama pull qwen3-coder:30b
```

### Python path on this machine

```
C:\Users\cjani\.local\bin\python3.14.exe
```

`python` and `python3` are not on PATH — always use the full path above in skill Bash calls.
