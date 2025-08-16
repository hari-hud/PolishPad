# ✨ PoliteText – AI-Powered Text Polisher

PoliteText helps you rephrase your messages into **clear, polite, and professional** language with one click.  
It works across apps (Slack, Outlook, Notes, Chrome, etc.) using macOS **Services / Quick Actions**.

---

## 🚀 Features
- Right-click any selected text → **Services → Polish with AI**.
- Polished text is returned immediately to your clipboard or inserted directly in place.  
- Works system-wide in most apps (Slack, Outlook, Mail, Notes, etc.).

---

## 🛠️ Installation

### 1. Clone or Download the Repo
```bash
git clone <your-repo-url>
cd polite-text
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup on macOS (Option 2: Quick Action)

### Step 1. Create Automator Quick Action
1. Open **Automator** → New → **Quick Action**.  
2. Set at the top:  
   - *Workflow receives current* → **text**  
   - *in* → **any application**  
3. Add **Run Shell Script**:  
   - *Pass input*: `as arguments`  
   - Script:  
     ```bash
     /usr/bin/python3 /path/to/polish_clipboard.py "$1"
     ```

### Step 2. Choose Insertion Method

#### Option A: Replace Selected Text (Recommended ✅)
- This will directly replace the highlighted text with polished text.  
- No extra permissions required.  
- Works reliably in most apps.

How:  
- In Automator Quick Action, set **Workflow receives text** → then select **Replace Selected Text** from the dropdown at the top right.  
- Done!

#### Option B: Insert Polished Text Below Original (Needs Accessibility)  
If you prefer the polished text to be inserted **under the original** instead of replacing it:  

1. After the **Run Shell Script**, add **Run AppleScript** with:
   ```applescript
   on run {input, parameters}
       tell application "System Events"
           keystroke return
           keystroke input
       end tell
       return input
   end run
   ```
2. Enable permissions:  
   - Go to **System Settings → Privacy & Security → Accessibility**  
   - Allow: **Automator**, **System Events**, **WorkflowServiceRunner**.  

⚠️ Some sandboxed apps may block simulated keystrokes.

---

## ▶️ Usage
1. Select text in Slack / Outlook / any app.  
2. Right-click → **Services → Polish with AI**.  
3. Either:  
   - Selected text is replaced with polished text (Option A), OR  
   - Polished text is inserted below the original (Option B).  

---

## 🔍 Logs & Debugging

### View Logs in Console.app
- Open **Console.app** (⌘+Space → "Console").  
- Filter for `Automator` or `WorkflowServiceRunner`.  

### Log to File (Optional)
You can enable logging to a file by editing `polish_clipboard.py` and adding:  
```python
import pathlib, datetime
logfile = pathlib.Path.home() / "polish_clipboard.log"
def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{ts}] {msg}\n")
```  
Then watch logs with:  
```bash
tail -f ~/polish_clipboard.log
```

---

## 🔄 Enable / Disable the Service

### Enable
- System Settings → Keyboard → Keyboard Shortcuts → Services  
- Scroll to find **Polish with AI** → ✅ check it.  
- (Optional) Assign a hotkey (e.g., ⌘⌥P).  

### Disable
- Uncheck the service in System Settings, OR  
- Delete it from:  
  ```
  ~/Library/Services/Polish with AI.workflow
  ```

---

## 🎯 Example

Original (Slack message):  
```
send me report asap
```

Polished:  
```
Could you please share the report at your earliest convenience?
```

---

Enjoy writing better messages with **PoliteText** ✨
