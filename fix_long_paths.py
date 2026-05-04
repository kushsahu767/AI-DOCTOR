import subprocess
import sys
import os
import ctypes

def is_admin():
    """Check if script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def enable_long_paths():
    """Enable Windows Long Path support"""
    if not is_admin():
        print("ERROR: This script needs to run as Administrator!")
        print("\nPlease do one of the following:")
        print("\n1. Run Command Prompt as Administrator and execute:")
        print("   C:\\Windows\\System32\\cmd.exe /c reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f")
        print("\n2. Or open PowerShell as Administrator and run:")
        print("   New-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem' -Name 'LongPathsEnabled' -Value 1 -PropertyType DWORD -Force")
        print("\nAfter that, come back and run: pipenv install")
        sys.exit(1)
    
    try:
        result = subprocess.run(
            ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem',
             '/v', 'LongPathsEnabled', '/t', 'REG_DWORD', '/d', '1', '/f'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✓ Long Path support enabled successfully!")
            print("\nNow you can install elevenlabs with:")
            print("  pipenv install elevenlabs")
        else:
            print("ERROR:", result.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    enable_long_paths()
