import os
import base64
from pathlib import Path

# Load `.env` file from the same directory as this script
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from groq import Groq

# Get API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        f"GROQ API key not found. Please ensure GROQ_API_KEY is set in {env_path}"
    )

client = Groq(api_key=api_key)
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image string
        
    Raises:
        FileNotFoundError: If the image file is not found
        IOError: If the file cannot be read
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at: {image_path}")
    except IOError as e:
        raise IOError(f"Error reading image file: {e}")

# Use the function
image_path = "D:\\local disk c copies\\download\\AI Mediacl Vision Chatbot\\acne.jpg"
encoded_image = encode_image_to_base64(image_path)
query = "What skin condition does this patient have?"
model = GROQ_MODEL

def create_chat_completion(query, encoded_image, model):
    """
    Create a chat completion with vision capability.
    
    Args:
        query (str): The question to ask about the image
        encoded_image (str): Base64 encoded image string
        model (str): Model to use for completion
        
    Returns:
        ChatCompletion: The completion response from Groq
    """
    messages = [
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
    
    chat_completions = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.6,
        max_completion_tokens=2048,
        top_p=0.95,
        reasoning_effort="default",
        stream=True,
    )
    return "".join(
        chunk.choices[0].delta.content or ""
        for chunk in chat_completions
    )

# Main execution
if __name__ == "__main__":
    result = create_chat_completion(query, encoded_image, model)
    print(result)