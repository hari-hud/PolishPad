
#!/usr/bin/env python3
"""
Polish Clipboard Tool
Copy -> Hotkey -> Paste

Hotkeys:
  - Polish: Ctrl+Shift+P (Win/Linux) or Cmd+Shift+P (macOS)
  - Next suggestion: Ctrl+Shift+] or Cmd+Shift+]
  - Quit: Ctrl+Shift+Q or Cmd+Shift+Q

Env vars:
  OPENAI_API_KEY   : required if POLISH_PROVIDER=openai
  POLISH_PROVIDER  : "openai" (default) or "ollama"
  POLISH_MODEL     : default "gpt-4o-mini" (OpenAI) or "llama3.1:8b" (Ollama)
  POLISH_ALTS      : number of suggestions to generate (default 3)
  POLISH_TONE      : "polite" (default), or "formal", "friendly", "concise"
  POLISH_TEMP      : float temperature 0-2 (default 0.4)
  POLISH_MAX_CHARS : max input characters to send (default 4000)
"""
import os
import sys
from typing import List, Optional

import pyperclip
from pynput import keyboard

# ---------------- Config ----------------
PROVIDER = os.getenv("POLISH_PROVIDER", "openai").lower()
MODEL = os.getenv("POLISH_MODEL") or ("gpt-4o-mini" if PROVIDER == "openai" else "llama3.1:8b")
NUM_ALTS = int(os.getenv("POLISH_ALTS", "3"))
TONE = os.getenv("POLISH_TONE", "polite").lower()
TEMP = float(os.getenv("POLISH_TEMP", "0.4"))
MAX_CHARS = int(os.getenv("POLISH_MAX_CHARS", "4000"))

SYSTEM_PROMPT = """You rephrase text to be clearer, simpler, and more polite while preserving meaning.
Rules:
- Keep original intent; do not add commitments or change facts.
- Prefer concise, plain language.
- Default tone: polite, professional. If asked, adapt tone: formal/friendly/concise.
- Return ONLY the rewritten text with no preamble, quotes, or bullet points.
"""

def _print_banner():
    print("Polish Clipboard Tool is running.")
    print("Press Ctrl+Shift+P (Cmd+Shift+P on macOS) to polish copied text.")
    print("Press Ctrl+Shift+] (Cmd+Shift+]) to cycle suggestions, Ctrl+Shift+Q to quit.")
    print(f"Provider: {PROVIDER}  Model: {MODEL}  Tone: {TONE}  Alts: {NUM_ALTS}  Temp: {TEMP}")
    sys.stdout.flush()

# --------------- Providers --------------
class ProviderBase:
    def rephrase(self, text: str, n: int = 3, tone: str = "polite", temperature: float = 0.4) -> List[str]:
        raise NotImplementedError

class OpenAIProvider(ProviderBase):
    def __init__(self, model: str):
        try:
            from openai import OpenAI  # type: ignore
        except Exception as e:
            raise RuntimeError("OpenAI Python package not installed. Run: pip install openai") from e
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set. Please export your API key.")
        self.client = OpenAI()
        self.model = model

    def rephrase(self, text: str, n: int = 3, tone: str = "polite", temperature: float = 0.4) -> List[str]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Tone: {tone}\n\nText:\n{text.strip()}"}
        ]
        # Use Chat Completions to get multiple choices (n)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            n=n,
            temperature=temperature,
        )
        outputs = []
        for choice in resp.choices:
            content = (choice.message.content or "").strip()
            if content:
                outputs.append(content)
        # Fallback: ensure at least 1 output
        return outputs or [text]

class OllamaProvider(ProviderBase):
    def __init__(self, model: str):
        try:
            import ollama  # type: ignore
            self.ollama = ollama
        except Exception as e:
            raise RuntimeError("Ollama Python package not installed. Run: pip install ollama") from e
        self.model = model

    def rephrase(self, text: str, n: int = 3, tone: str = "polite", temperature: float = 0.4) -> List[str]:
        # We'll make n calls; Ollama doesn't support 'n' directly.
        outputs = []
        for _ in range(max(1, n)):
            r = self.ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Tone: {tone}\n\nText:\n{text.strip()}"}
                ],
                options={"temperature": temperature}
            )
            content = (r.get("message", {}).get("content") or "").strip()
            if content:
                outputs.append(content)
        return outputs or [text]

def get_provider(name: str, model: str) -> ProviderBase:
    if name == "openai":
        return OpenAIProvider(model)
    elif name == "ollama":
        return OllamaProvider(model)
    else:
        raise RuntimeError(f"Unknown provider '{name}'. Use 'openai' or 'ollama'.")

# -------------- App State ---------------
last_source: Optional[str] = None
alternatives: List[str] = []
alt_index: int = 0
provider: ProviderBase = get_provider(PROVIDER, MODEL)

def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "…"

def polish_text(text: str, tone: str = TONE, n: int = 1, temperature: float = TEMP) -> str:
    """
    Rephrase given text using the selected provider.
    Returns the first polished suggestion (string).
    """
    text = text.strip()
    if not text:
        return ""
    text = _truncate(text, MAX_CHARS)
    try:
        results = provider.rephrase(text, n=n, tone=tone, temperature=temperature)
        return results[0] if results else text
    except Exception as e:
        print(f"Error in polish_text: {e}")
        return text
    
def polish_from_clipboard():
    global last_source, alternatives, alt_index
    src = pyperclip.paste()
    if not src or not src.strip():
        print("Clipboard is empty. Copy some text first.")
        return
    # If current clipboard equals current polished suggestion, treat as cycle press
    if alternatives and src.strip() == (alternatives[alt_index].strip() if alternatives else "").strip():
        _cycle_suggestion()
        return

    clean = src.strip()
    clean = _truncate(clean, MAX_CHARS)
    print(f"Polishing {len(clean)} chars (tone={TONE}, alts={NUM_ALTS})…")
    try:
        alternatives = provider.rephrase(clean, n=NUM_ALTS, tone=TONE, temperature=TEMP)
        alt_index = 0
        pyperclip.copy(alternatives[alt_index])
        print(f"[1/{len(alternatives)}] Copied polished text to clipboard:\n{alternatives[alt_index]}\n")
        last_source = clean
    except Exception as e:
        print(f"Error during polish: {e}")

def _cycle_suggestion():
    global alt_index, alternatives
    if not alternatives:
        print("No suggestions to cycle. Trigger a polish first.")
        return
    alt_index = (alt_index + 1) % len(alternatives)
    pyperclip.copy(alternatives[alt_index])
    print(f"[{alt_index+1}/{len(alternatives)}] Copied next suggestion.\n{alternatives[alt_index]}\n")

def _on_quit():
    print("Quitting…")
    os._exit(0)

def main():
    _print_banner()
    combo_polish_win = "<ctrl>+<shift>+p"
    combo_polish_mac = "<cmd>+<shift>+p"
    combo_next_win = "<ctrl>+<shift>+]"
    combo_next_mac = "<cmd>+<shift>+]"
    combo_quit_win = "<ctrl>+<shift>+q"
    combo_quit_mac = "<cmd>+<shift>+q"

    hotkeys = {
        combo_polish_win: polish_from_clipboard,
        combo_polish_mac: polish_from_clipboard,
        combo_next_win: _cycle_suggestion,
        combo_next_mac: _cycle_suggestion,
        combo_quit_win: _on_quit,
        combo_quit_mac: _on_quit,
    }

    with keyboard.GlobalHotKeys(hotkeys) as h:
        h.join()

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         pass

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Text passed as argument (from Automator)
        input_text = sys.argv[1]
        polished = polish_text(input_text)
        print(polished)
    else:
        # Fallback to clipboard workflow
        main()
