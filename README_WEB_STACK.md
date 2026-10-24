# Web stack

The repository now contains a small three-service web architecture:

```text
frontend/       React + Vite UI
history-service Java Spring Boot + PostgreSQL history API
ai-service/     FastAPI AI analysis API
```

## Start PostgreSQL

```powershell
docker compose up -d postgres
```

## Start the Java history service

Install Maven and PostgreSQL (or Docker Desktop), then start the database.
If using the included Docker Compose file:

```powershell
cd E:\Git_Hub\AI-DOCTOR
docker compose up -d postgres
```

Install Maven, then run from `history-service`:

```powershell
cd E:\Git_Hub\AI-DOCTOR\history-service
mvn spring-boot:run
```

The API runs on `http://localhost:8080`.

## Start the Python AI service

```powershell
cd E:\Git_Hub\AI-DOCTOR
.\.venv312\Scripts\Activate.ps1
pip install -r ai-service\requirements.txt
uvicorn main:app --app-dir ai-service --reload --port 8000
```

The API runs on `http://localhost:8000`.

## Start the React frontend

In another terminal:

```powershell
cd E:\Git_Hub\AI-DOCTOR\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The frontend currently supports patient creation, image/PDF upload, voice recording, detailed AI analysis, required ElevenLabs voice playback, and consultation history. A consultation is not completed until ElevenLabs returns valid MP3 audio. API keys remain in the root `.env` and are loaded only by the Python service.
