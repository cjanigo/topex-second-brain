#!/usr/bin/env python3
"""
Utility: call a local Ollama model and print the response to stdout.

Usage:
    python ollama_query.py --prompt "Your prompt here"
    python ollama_query.py --prompt "..." --model mistral --system "You are a helper."
    python ollama_query.py --prompt "..." --url http://localhost:11434

Exit codes:
    0 — success, response printed to stdout
    1 — error (Ollama not running, model not found, etc.), details on stderr
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser(description="Query a local Ollama model.")
    parser.add_argument("--prompt", required=True, help="User prompt to send")
    parser.add_argument("--model", default="qwen3-coder:30b", help="Ollama model name (default: qwen3-coder:30b)")
    parser.add_argument("--system", default="", help="Optional system prompt")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama base URL (default: http://localhost:11434)")
    args = parser.parse_args()

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.prompt})

    payload = {
        "model": args.model,
        "messages": messages,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    endpoint = args.url.rstrip("/") + "/api/chat"

    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(result["message"]["content"])
    except urllib.error.URLError as e:
        print(f"Error: could not reach Ollama at {endpoint} — {e.reason}", file=sys.stderr)
        print("Is Ollama running? Try: ollama serve", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print("Error: unexpected response format from Ollama.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
