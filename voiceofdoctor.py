import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== Google Text-to-Speech (gTTS) =====
try:
    from gtts import gTTS
except ModuleNotFoundError:
    print("gtts module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts"])
    from gtts import gTTS

def texttospeech_gtts(text, output_file):
    """Convert text to speech using Google TTS"""
    try:
        language = "en"
        audioobject = gTTS(
            text=text,
            lang=language,
            slow=False
        )
        audioobject.save(output_file)
        print(f"✓ gTTS audio saved: {output_file}")
    except Exception as e:
        print(f"gTTS Error: {e}")

# ===== ElevenLabs Text-to-Speech =====
def texttospeech_elevenlabs(text, output_file):
    """Convert text to speech using ElevenLabs (Free Tier - requires custom voice)"""
    try:
        from elevenlabs.client import ElevenLabs
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:   
            print("ERROR: ELEVENLABS_API_KEY not found. Please set it in the .env file.")
            return False
        
        client = ElevenLabs(api_key=api_key)
        
        # For FREE TIER: You need a custom voice ID from your account
        # Go to: https://elevenlabs.io/app/voice-lab and create/clone a voice
        # Then use that voice_id here
        
        # Try to get custom voice ID from environment, otherwise use default
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", None)
        
        if not voice_id:
            print("⚠️  ELEVENLABS_VOICE_ID not set.")
            print("\n📋 To use ElevenLabs free tier:")
            print("   1. Go to: https://elevenlabs.io/app/voice-lab")
            print("   2. Create or clone a custom voice")
            print("   3. Copy the Voice ID")
            print("   4. Add to .env: ELEVENLABS_VOICE_ID=your_voice_id_here")
            return False
        
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2"
        )
        
        with open(output_file, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"✓ ElevenLabs audio saved: {output_file}")
        return True
        
    except ModuleNotFoundError:
        print("ERROR: elevenlabs not properly installed.")
        print("Fix: Run 'pipenv install' or 'pip install elevenlabs==2.0.0'")
        return False
    except Exception as e:
        error_msg = str(e)
        if "library voices" in error_msg.lower() or "paid_plan" in error_msg.lower():
            print("\n❌ ERROR: Free tier limitation!")
            print("\n📝 The voice ID you provided is a LIBRARY voice (pre-made).")
            print("   Free tier can ONLY use custom voices you CREATE.")
            print("\n✅ To fix this:")
            print("   1. Go to: https://elevenlabs.io/app/voice-lab")
            print("   2. Click '+ Create a new voice'")
            print("   3. Record yourself speaking (5-30 seconds) - don't clone")
            print("   4. Name it and save")
            print("   5. Copy the NEW voice ID")
            print("   6. Update .env with: ELEVENLABS_VOICE_ID=your_new_custom_voice_id")
            print("\n📌 ALTERNATIVELY: Just use Google TTS (fully working)")
        else:
            print(f"ElevenLabs Error: {e}")
        return False

# ===== Main =====
if __name__ == "__main__":
    text = "Hi this is your AI Doctor, how can I help you today?"
    
    # Test Google TTS
    print("\n--- Testing Google Text-to-Speech ---")
    texttospeech_gtts(text, "gtts_output.mp3")
    
    # Test ElevenLabs TTS
    print("\n--- Testing ElevenLabs Text-to-Speech ---")
    texttospeech_elevenlabs(text, "elevenlabs_output.mp3")