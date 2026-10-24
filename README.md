# AI Doctor with Vision and Voice

AI Doctor is a multimodal healthcare-assistance project that accepts patient text,
voice recordings, images, and (in the web stack) PDF reports. It uses Groq for
speech transcription and AI analysis, and ElevenLabs or gTTS for voice output.

> **Medical disclaimer:** This project is for educational purposes only. It does
> not provide a medical diagnosis and is not a substitute for a qualified
> healthcare professional. Seek professional or emergency care when appropriate.

## Features

- Image analysis with a vision-capable Groq model
- Voice transcription using Groq Whisper
- Text and audio responses
- ElevenLabs voice generation with gTTS fallback in the Gradio app
- React web interface with patient and consultation history
- Spring Boot history service backed by PostgreSQL
- PDF report text extraction in the web AI service

## Project structure

```text
AI-DOCTOR/
├── gradioapp.py                 # Legacy Gradio application
├── brainofdoctor.py             # Standalone image-analysis example
├── voiceofdoctor.py             # ElevenLabs and gTTS helpers
├── voiceofpatient.py            # Standalone microphone/transcription example
├── requirements.txt             # Dependencies for the Gradio application
├── ai-service/
│   ├── main.py                  # FastAPI analysis and voice API
│   └── requirements.txt
├── history-service/
│   ├── pom.xml                  # Spring Boot service
│   └── src/
├── frontend/                    # React + Vite web client
├── docker-compose.yml            # PostgreSQL development database
└── README_WEB_STACK.md          # Additional web-stack notes
```

Generated files such as Python caches, `node_modules`, frontend builds, Maven
`target` output, and local environment files are intentionally ignored by Git.

## Prerequisites

### Gradio application

- Python 3.11 or newer
- A Groq API key
- An ElevenLabs API key and voice ID if ElevenLabs output is required
- FFmpeg and PortAudio may be required by the audio dependencies

### Web stack

- Python 3.11 or newer
- Node.js and npm
- Java 17
- Maven
- Docker Desktop, for the included PostgreSQL container

## Configuration

Create a `.env` file in the repository root. Do not commit it.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
```

The frontend uses these local development defaults:

```env
VITE_HISTORY_API_URL=http://localhost:8080/api
VITE_AI_API_URL=http://localhost:8000
```

If you need different URLs, create `frontend/.env.local` with those variables.
The committed [frontend/.env.example](frontend/.env.example) shows the variable
names without exposing credentials.

## Run the Gradio application

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the application:

```powershell
python gradioapp.py
```

Gradio prints the local URL in the terminal, normally
`http://127.0.0.1:7860`. The application accepts a voice recording and an image
of a skin condition, then returns text, transcription output, and generated
audio.

## Run the web stack

Start PostgreSQL:

```powershell
docker compose up -d postgres
```

### Start the AI service

From the repository root, install the service dependencies and start FastAPI:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r ai-service\requirements.txt
uvicorn main:app --app-dir ai-service --reload --port 8000
```

The AI service is available at `http://localhost:8000`. Its health endpoint is
`http://localhost:8000/health`.

### Start the history service

In a second terminal:

```powershell
cd history-service
mvn spring-boot:run
```

The history service is available at `http://localhost:8080`.

### Start the frontend

In a third terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`.

To create a production frontend build:

```powershell
npm run build
```

## API endpoints

The AI service currently exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/api/analyze` | Analyze symptoms, images, PDF reports, and audio |
| POST | `/api/speak` | Generate MP3 speech from analysis text |

The history service exposes patient and consultation endpoints under
`/api/patients` and `/api/consultations`.

## Development notes

- Keep API keys in the root `.env` file.
- Do not commit generated audio, build output, dependency directories, or
  compiled Java classes.
- AI responses are informational and should be reviewed by a healthcare
  professional.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request with a clear description.

## Author

Kush Sahu
