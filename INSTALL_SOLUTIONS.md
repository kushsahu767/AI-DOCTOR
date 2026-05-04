# SOLUTIONS FOR ELEVENLABS INSTALLATION

## **SOLUTION 1: Manual Registry Edit (No Admin Prompt)**

### For Windows 10/11:

1. Press **Win + R**
2. Type: `regedit` and press Enter
3. Click "Yes" if prompted
4. Navigate to: 
   ```
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   ```
5. Right-click in the empty space → **New** → **DWORD (32-bit) Value**
6. Name it: `LongPathsEnabled`
7. Double-click it and set value to: `1`
8. Click OK and close Registry Editor
9. No restart needed usually, but you can restart if needed

After this, run:
```bash
cd "d:\local disk c copies\download\AI Mediacl Vision Chatbot"
pipenv install elevenlabs
```

---

## **SOLUTION 2: Install Older elevenlabs Version (Simplest)**

Add this to your Pipfile manually, then run `pipenv install`:

```ini
[packages]
groq = "*"
python-dotenv = "*"
speechrecognition = "*"
pydub = "*"
pyaudio = "*"
gtts = "*"
elevenlabs = "==0.2.28"
```

Or install directly:
```bash
pipenv run pip install elevenlabs==0.2.28 --no-cache-dir
```

This older version has fewer nested modules and shouldn't have the long path issue.

---

## **SOLUTION 3: Use Python Script to Enable Long Paths**

Right-click Command Prompt → **Run as Administrator** → paste:
```cmd
python "d:\local disk c copies\download\AI Mediacl Vision Chatbot\fix_long_paths.py"
```

---

## **SOLUTION 4: Alternative - Use Google Text-to-Speech**

If you want to avoid elevenlabs entirely, update your code to use Google Cloud TTS or keep using gTTS (which you already have installed).

---

**RECOMMENDED: Try Solution 1 (Manual Registry Edit) first - it's the most reliable.**
