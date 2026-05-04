# How to Install ElevenLabs

Windows is preventing the installation of `elevenlabs` because it has file paths that exceed Windows' default 260-character limit.

## Solution: Enable Windows Long Path Support

### Option 1: Run the Batch File (Easiest - Recommended)

1. Double-click `enable_long_paths.bat` in the project folder
2. Click "Yes" when prompted for Administrator privileges
3. Wait for the success message
4. Then run: `pip install elevenlabs`

### Option 2: Run PowerShell Script

1. Right-click `enable_long_paths.ps1` → "Run with PowerShell" (as Administrator)
2. Then run: `pip install elevenlabs`

### Option 3: Manual Registry Edit

If you prefer to do it manually:
1. Press `Win + R`, type `regedit`
2. Navigate to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. Right-click → New → DWORD Value
4. Name it: `LongPathsEnabled`
5. Set value to: `1`
6. Restart (optional, not usually needed)

### After Enabling Long Paths

Install elevenlabs with:
```bash
pip install elevenlabs
```

Or use pipenv:
```bash
pipenv install elevenlabs
```

## What Does This Do?

This enables Windows to support file paths longer than 260 characters. Some Python packages (like elevenlabs) have deeply nested module structures that require this support.
