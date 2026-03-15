# Local Model Setup

The local model handles cheap, fast, offline tasks — no API tokens burned.

## Requirements
- [Ollama](https://ollama.ai) installed
- At least 8GB RAM (7B model)
- ~5GB disk space

## Setup

```bash
# 1. Pull the base model
ollama pull qwen2.5-coder:7b

# 2. Copy and fill in the template
cp ollama/Modelfile.template ollama/Modelfile
# Edit ollama/Modelfile — fill in [YOUR NAME/HANDLE] and your stack

# 3. Create the model
ollama create my-coder -f ollama/Modelfile

# 4. Test it
ollama run my-coder "What is your role?"
```

## Alternative base models

| Model | Size | Best for |
|-------|------|----------|
| qwen2.5-coder:7b | 4.7GB | Code (recommended) |
| qwen2.5-coder:14b | 9GB | Code, more capable |
| mistral:7b | 4.4GB | General tasks |
| deepseek-coder-v2:16b | 9GB | Complex code |

## What to send here

See agents/local-router.md for the full routing table.
Short version: CSS, config, env files, boilerplate, small refactors.

## Cursor integration

In Cursor: Settings → Models → Add Model → point to `http://localhost:11434`
Select your model name in the model picker when on local tasks.
