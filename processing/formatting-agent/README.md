# Tech Searches Formatting Agent

This agent processes notes from the `preformatted/` directory and formats them according to the system prompt using Ollama's qwen2.5:14b model.

## Setup

1. **Install dependencies:**
   ```bash
   cd processing/formatting-agent
   uv venv venv
   source venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Ensure Ollama is running:**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   ```

## Usage

### Process all files in preformatted directory:
```bash
source venv/bin/activate
python3 format_notes.py
```

### Process a specific file:
```bash
source venv/bin/activate
python3 format_notes.py --file filename.md
```

### List available files:
```bash
source venv/bin/activate
python3 format_notes.py --list-files
```

### Use a different model:
```bash
source venv/bin/activate
python3 format_notes.py --model llama3.1:8b-instruct-q6_K
```

## Available Models

Based on your Ollama installation:
- `qwen2.5:14b-instruct-q5_K_M` (default - best for text formatting)
- `llama3.1:8b-instruct-q6_K`
- `qwen2.5:7b`
- `deepseek-r1:14b`
- `gemma3:12b`
- `mistral:latest`

## Output

Formatted files are saved to the `autoformatted/` directory with metadata headers indicating:
- Original filename
- Processing timestamp
- Model used
- Agent information

## System Prompt

The agent uses the system prompt from `system-prompt.md` to convert raw notes into well-formatted stack research definitions.
