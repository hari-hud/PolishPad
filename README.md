# PolishPad - AI-Powered Text Polisher

A small cross‑platform Python tool that polishes any copied text (simpler, clear, polite).
Workflow: **Copy → Hotkey → Paste**.

## Hotkeys
- **Polish**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
- **Next suggestion**: `Ctrl+Shift+]` or `Cmd+Shift+]`
- **Quit**: `Ctrl+Shift+Q` or `Cmd+Shift+Q`

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set your provider (OpenAI by default) and API key
export OPENAI_API_KEY="sk-..."            # Windows PowerShell: setx OPENAI_API_KEY "sk-..."
export POLISH_PROVIDER="openai"           # or "ollama"
export POLISH_MODEL="gpt-4o-mini"         # ollama example: "llama3.1:8b"

python polish_clipboard.py
```

On Linux you may need `xclip` or `xsel` for clipboard:
```bash
sudo apt-get install xclip  # or: sudo apt-get install xsel
```

On macOS, grant **Accessibility** permission to Terminal/iTerm/Python:
System Settings → Privacy & Security → Accessibility → enable for your terminal app.
