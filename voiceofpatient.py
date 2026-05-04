#step1: setup audio recorder (ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
import os
from io import BytesIO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def record_audio_simple(file_path,timeout=20,phrase_time_limit=60):
    """Simplified function to record audio from the microphone and save it to the it as an MP3 FILE.
    args:
    file_path: path to save the recorded audio file
    timeout: maximum time to wait for a phrase to start (in seconds)
    phrase_time_limit: maximum time for each phrase to be recorded(in seconds).
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Please speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            logging.info("Listening for audio...")
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete, processing audio...")
            
            # Save the audio data to a WAV file
            wav_data = audio_data.get_wav_data()
            logging.info(f"Audio data size: {len(wav_data)} bytes")
            
            if len(wav_data) == 0:
                logging.error("No audio data captured. Please check your microphone.")
                return False
            
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            
            # Save as WAV format
            wav_path = file_path.replace(".mp3", ".wav")
            audio_segment.export(wav_path, format="wav")
            logging.info(f"Audio saved to {wav_path} (WAV format)")
            return True

    except sr.UnknownValueError:
        logging.error("Could not understand audio. Please speak more clearly.")
        return False
    except sr.RequestError as e:
        logging.error(f"Could not request results from speech recognition service: {e}")
        return False
    except Exception as e:
        logging.error(f"An error occurred while recording audio: {e}")
        return False
        

recording_success = record_audio_simple(file_path="patient_voice_test.wav")

if not recording_success:
    logging.error("Failed to record audio. Exiting...")
    exit(1)

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logging.error("GROQ_API_KEY not found. Please add it to the .env file.")
    exit(1)
stt_model = "whisper-large-v3"
def transcribe_audio(file_path):
    client = Groq(api_key=GROQ_API_KEY)
    

    try:
        audio_path = "patient_voice_test.wav"
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            logging.info(f"Audio file size: {file_size} bytes")
            
            if file_size == 0:
                logging.error("Audio file is empty. Recording failed.")
            else:
                with open(audio_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=audio_file,
                        model=stt_model
                    )
                # Extract the text from the transcription object
                transcribed_text = transcription.text
                print("Transcription:", transcribed_text)
        else:
            logging.error("Audio file not found. Recording may have failed.")
    except Exception as e:
        logging.error(f"Error during transcription: {e}")

        
