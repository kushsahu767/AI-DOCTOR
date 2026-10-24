import os
import base64
import gradio as gr
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import io
import numpy as np

# Load environment
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from groq import Groq
from voiceofdoctor import texttospeech_elevenlabs, texttospeech_gtts

# Initialize API client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

def encode_image_to_base64(image_input):
    """Encode an image file or PIL Image or numpy array to base64 string."""
    try:
        # If it's a numpy array (from Gradio), convert to PIL Image
        if isinstance(image_input, np.ndarray):
            print(f"Converting numpy array (shape: {image_input.shape}) to PIL Image...")
            image_input = Image.fromarray(image_input.astype('uint8'))
        
        # If it's a string path, read from file
        if isinstance(image_input, str):
            print(f"Reading image from file: {image_input}")
            with open(image_input, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
        
        # If it's a PIL Image, convert to base64
        if isinstance(image_input, Image.Image):
            print("Encoding PIL Image to base64...")
            image_input = image_input.convert("RGB")
            image_input.thumbnail((1024, 1024))
            buffered = io.BytesIO()
            image_input.save(buffered, format="JPEG", quality=85, optimize=True)
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            print(f"Image encoded successfully. Size: {len(encoded_image)} bytes")
            return encoded_image
        
        # If it's bytes
        if isinstance(image_input, bytes):
            print("Encoding bytes to base64...")
            encoded_image = base64.b64encode(image_input).decode("utf-8")
            return encoded_image
        
        print(f"ERROR: Unexpected image type: {type(image_input)}")
        return None
        
    except Exception as e:
        print(f"Error encoding image: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_chat_completion(query, encoded_image, model):
    """Create chat completion with vision capability."""
    if not encoded_image:
        return "⚠️ Error: Could not process image. Please upload a clear JPEG or PNG image."
    
    messages = [
        {
            "role": "system",
            "content": (
                "Answer concisely in plain text while preserving Markdown exactly. "
                "Keep headings beginning with #, bold markers **, bullet markers -, "
                "numbering, emojis, and other symbols in your response."
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ],
        }
    ]
    
    try:
        chat_completions = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.6,
            max_completion_tokens=768,
            top_p=0.9,
            reasoning_effort="low",
            stream=True,
        )
        return "".join(
            chunk.choices[0].delta.content or ""
            for chunk in chat_completions
        )
    except Exception as e:
        error_msg = str(e)
        print(f"API Error: {error_msg}")
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            return "⚠️ API Authentication Error. Check your GROQ_API_KEY in .env file."
        else:
            return f"⚠️ Doctor's Analysis Error: {error_msg}"

def process_input(audio_input, image_input):
    """Process voice and image input from user."""
    doctor_response = "Welcome to AI Medical Vision Chatbot!"
    transcribed_text = ""
    audio_output_path = None
    
    try:
        # Process image if provided
        if image_input is not None:
            print(f"Image received - Type: {type(image_input)}")
            encoded_image = encode_image_to_base64(image_input)
            
            if encoded_image:
                query = (
                    "Analyze this skin image. Provide a concise response with: "
                    "# Possible condition, # Observations, # Recommended next steps, "
                    "and a brief safety disclaimer. Do not remove Markdown symbols."
                )
                model = GROQ_MODEL
                print("Sending to Groq API for analysis...")
                doctor_response = create_chat_completion(query, encoded_image, model)
                print(f"Doctor response received: {doctor_response[:100]}...")
            else:
                doctor_response = "⚠️ Unable to process the image. Please upload a clear image of the skin condition."
        
        # Process audio if provided
        if audio_input is not None:
            print(f"Audio received - Type: {type(audio_input)}")
            transcribed_text = f"Audio received: {audio_input}"
        
        # Generate voice response
        if doctor_response and doctor_response != "Welcome to AI Medical Vision Chatbot!":
            try:
                audio_output_path = "doctor_response.mp3"
                elevenlabs_success = texttospeech_elevenlabs(
                    doctor_response,
                    output_file=audio_output_path,
                )
                if not elevenlabs_success:
                    texttospeech_gtts(doctor_response, output_file=audio_output_path)
                print("Voice response generated successfully")
            except Exception as e:
                print(f"TTS Error: {e}")
        
        return doctor_response, transcribed_text, audio_output_path
    
    except Exception as e:
        print(f"Error in process_input: {str(e)}")
        return f"Error processing input: {str(e)}", "", None


iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(label="Patient's Voice Input"),
        gr.Image(label="Patient's Skin Condition Image")
    ],
    outputs=[
        gr.Textbox(label="Doctor's Response"),
        gr.Textbox(label="Transcribed Patient Audio"),
        gr.Audio(label="Doctor's Voice Response")
    ],
    title="AI Medical Vision Chatbot",
    description="An AI Doctor that can see your skin condition and listen to your voice to provide medical advice. Please speak clearly and upload a clear image of your skin condition for the best results."
)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏥 AI Medical Vision Chatbot is starting...")
    print("="*60)
    iface.launch(debug=False, share=True)



