import base64
import io
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import Groq
from elevenlabs.client import ElevenLabs
from pypdf import PdfReader

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

app = FastAPI(title="AI Doctor Analysis Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured")
    return Groq(api_key=api_key)


def get_elevenlabs_client() -> ElevenLabs:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY is not configured")
    return ElevenLabs(api_key=api_key)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-service"}


@app.post("/api/analyze")
async def analyze(
    symptoms: str = Form(""),
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None),
) -> dict[str, str]:
    if not symptoms.strip() and image is None and audio is None:
        raise HTTPException(status_code=400, detail="Provide symptoms, an image, a PDF, or audio")

    transcript = ""
    if audio is not None:
        audio_bytes = await audio.read()
        if not audio_bytes:
            raise HTTPException(status_code=422, detail="The audio recording is empty")
        try:
            transcription = get_client().audio.transcriptions.create(
                file=(audio.filename or "patient-recording.webm", audio_bytes),
                model="whisper-large-v3",
                response_format="json",
            )
            transcript = transcription.text.strip()
        except Exception as error:
            raise HTTPException(status_code=502, detail=f"Audio transcription failed: {error}") from error

    content: list[dict] = [{"type": "text", "text": (
        "Analyze the patient input conservatively and in useful detail. Return plain text "
        "with these exact sections: Summary, Key observations, Results explained, "
        "Risk indicators, Recommended next steps, and When to seek urgent care. "
        "Explain medical terms in simple language, identify values that may need professional "
        "review, and distinguish reported facts from general possibilities. Do not diagnose "
        "or predict with certainty; advise professional care when needed.\n\n"
        f"Patient input: {symptoms or 'No text provided.'}\n"
        f"Patient voice transcript: {transcript or 'No voice recording provided.'}"
    )}]

    if image is not None:
        image_bytes = await image.read()
        if image.content_type == "application/pdf":
            reader = PdfReader(io.BytesIO(image_bytes))
            report_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            if not report_text.strip():
                raise HTTPException(status_code=422, detail="Could not extract text from PDF")
            content[0]["text"] += f"\n\nMedical report:\n{report_text[:30000]}"
        elif image.content_type and image.content_type.startswith("image/"):
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": (
                        f"data:{image.content_type};base64,"
                        f"{base64.b64encode(image_bytes).decode('utf-8')}"
                    )
                },
            })
        else:
            raise HTTPException(status_code=415, detail="Only images and PDF files are supported")

    try:
        response = get_client().chat.completions.create(
            model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
            messages=[{"role": "user", "content": content}],
            temperature=0.3,
            max_completion_tokens=768,
            reasoning_effort="low",
        )
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {error}") from error
    return {"summary": response.choices[0].message.content or "", "transcript": transcript}


@app.post("/api/speak")
async def speak(text: str = Form(...)):
    clean_text = text.strip()
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text for voice generation is required")
    if not voice_id:
        raise HTTPException(status_code=500, detail="ELEVENLABS_VOICE_ID is not configured")

    try:
        audio = get_elevenlabs_client().text_to_speech.convert(
            text=clean_text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2",
            optimize_streaming_latency=4,
            output_format="mp3_44100_128",
        )
        return StreamingResponse(audio, media_type="audio/mpeg")
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"ElevenLabs voice generation failed: {error}") from error
