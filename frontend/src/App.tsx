import { FormEvent, useEffect, useRef, useState } from "react";

const historyApi = import.meta.env.VITE_HISTORY_API_URL ?? "http://localhost:8080/api";
const aiApi = import.meta.env.VITE_AI_API_URL ?? "http://localhost:8000";

type Patient = { id: number; name: string; age?: number; gender?: string };
type Consultation = {
  id: number;
  symptoms: string;
  aiSummary?: string;
  riskLevel?: string;
  createdAt: string;
};

export default function App() {
  const [view, setView] = useState<"landing" | "dashboard">("landing");
  const [patient, setPatient] = useState<Patient | null>(null);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [history, setHistory] = useState<Consultation[]>([]);
  const [name, setName] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [voice, setVoice] = useState<File | null>(null);
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const recorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const [analysis, setAnalysis] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    fetch(`${historyApi}/patients`).then(async (response) => {
      if (response.ok) setPatients(await response.json());
    }).catch(() => setError("History service is not running."));
  }, []);

  async function createPatient(event: FormEvent) {
    event.preventDefault();
    setError("");
    const response = await fetch(`${historyApi}/patients`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!response.ok) return setError("Could not create patient.");
    const created = await response.json();
    setPatient(created);
    setPatients((items) => [created, ...items]);
    setName("");
  }

  async function loadHistory(selected: Patient) {
    setPatient(selected);
    const response = await fetch(`${historyApi}/patients/${selected.id}/consultations`);
    if (response.ok) setHistory(await response.json());
  }

  async function analyze(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setNotice("");
    setAnalysis("");
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
      setAudioUrl("");
    }
    const data = new FormData();
    data.append("symptoms", symptoms);
    if (image) data.append("image", image);
    if (voice) data.append("audio", voice);
    try {
      const response = await fetch(`${aiApi}/api/analyze`, { method: "POST", body: data });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.detail ?? "AI analysis failed.");
      setAnalysis(result.summary);
      setTranscript(result.transcript ?? "");
      const voiceResponse = await fetch(`${aiApi}/api/speak`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ text: result.summary }),
      });
      if (!voiceResponse.ok) {
        const voiceResult = await voiceResponse.json().catch(() => ({}));
        throw new Error(voiceResult.detail ?? "ElevenLabs voice generation failed.");
      }
      const audioBlob = await voiceResponse.blob();
      if (!audioBlob.size || audioBlob.type !== "audio/mpeg") {
        throw new Error("ElevenLabs returned an invalid audio response.");
      }
      setAudioUrl(URL.createObjectURL(audioBlob));
      if (patient) {
        const historyResponse = await fetch(`${historyApi}/patients/${patient.id}/consultations`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            symptoms: symptoms || "Image/report analysis",
            aiSummary: result.summary,
            riskLevel: "Review required",
          }),
        });
        if (!historyResponse.ok) {
          const historyResult = await historyResponse.json().catch(() => ({}));
          throw new Error(historyResult.message ?? "Analysis completed, but history could not be saved.");
        }
        await loadHistory(patient);
      }
    } catch (reason) {
      setError(
        reason instanceof TypeError
          ? "Could not connect to the AI service. Confirm that FastAPI is running on port 8000."
          : reason instanceof Error
            ? reason.message
            : "AI analysis failed.",
      );
    } finally {
      setBusy(false);
    }
  }

  async function toggleRecording() {
    if (recording) {
      recorder.current?.stop();
      setRecording(false);
      return;
    }
    if (!navigator.mediaDevices?.getUserMedia) {
      setError("Microphone recording is not supported by this browser.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const nextRecorder = new MediaRecorder(stream);
      chunks.current = [];
      nextRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunks.current.push(event.data);
      };
      nextRecorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        setVoice(new File(chunks.current, "patient-recording.webm", { type: "audio/webm" }));
      };
      recorder.current = nextRecorder;
      nextRecorder.start();
      setRecording(true);
      setError("");
    } catch {
      setError("Microphone permission was denied or is unavailable.");
    }
  }

  if (view === "landing") {
    return (
      <main className="health-landing">
        <nav className="health-nav">
          <button className="health-brand" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}><span>✚</span> AI Doctor</button>
          <div className="health-links"><a href="#care">Our approach</a><a href="#features">Capabilities</a><a href="#story">About us</a></div>
          <button className="nav-dashboard" onClick={() => setView("dashboard")}>Go to dashboard <span>↗</span></button>
        </nav>
        <section className="health-hero" id="care">
          <div className="hero-content">
            <div className="hero-kicker"><span /> FOR PEOPLE WHO WANT TO UNDERSTAND THEIR HEALTH</div>
            <h1>Healthcare for<br /><strong>personalised</strong><br />wellness solutions<span>!</span></h1>
            <p>AI Doctor brings your symptoms, reports, and health questions together in one calm, clear place.</p>
            <div className="hero-buttons"><button className="hero-dashboard" onClick={() => setView("dashboard")}>Go to dashboard <span>→</span></button><button className="watch-button" onClick={() => document.getElementById("story")?.scrollIntoView({ behavior: "smooth" })}>Watch how it works <span>→</span></button></div>
          </div>
          <div className="hero-visual">
            <div className="hero-photo"><div className="doctor-illustration"><span className="doctor-head">◉</span><span className="doctor-body">✚</span></div><div className="family-shape"><span>◯</span><span>◯</span></div></div>
            <div className="hero-tag tag-department"><span>♥</span> AI-assisted care</div>
            <div className="hero-tag tag-patients"><span>✦</span> Clear health insights</div>
            <div className="hero-appointment"><strong>Ready when you are</strong><span>Upload a report or describe how you feel.</span><button onClick={() => setView("dashboard")}>↗</button></div>
          </div>
          <div className="hero-scroll">SCROLL TO EXPLORE <span>↓</span></div>
        </section>
        <section className="health-story" id="story">
          <div className="section-title"><span>Our perspective</span><h2>World of health</h2></div>
          <div className="story-copy"><p>Embark on a more informed health journey. Our commitment to accessible, understandable care goes beyond a single answer.</p><blockquote>“Your health story is personal. AI Doctor helps you make sense of every chapter with thoughtful guidance.”</blockquote><button className="read-more" onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}>Read more <span>↗</span></button></div>
        </section>
        <section className="health-features" id="features">
          <article className="feature-card feature-orbit"><span className="feature-icon">◉</span><h3>One place for your health story</h3><p>Bring symptoms, images, reports, and voice notes into one simple consultation.</p><button onClick={() => setView("dashboard")}>Explore <span>→</span></button></article>
          <article className="feature-card feature-image"><span className="feature-label">#AI ASSISTANT</span><h3>Not just information.<br />A clearer next step.</h3><button onClick={() => setView("dashboard")}>Try it <span>→</span></button></article>
          <article className="feature-card feature-care"><span className="feature-label">YOUR CARE, YOUR CONTROL</span><h3>Understand more.<br />Feel more prepared.</h3><button onClick={() => setView("dashboard")}>Start now <span>→</span></button></article>
        </section>
        <section className="health-trust">
          <div><strong>Built around better conversations</strong><span>Thoughtful technology for the moments when health information feels overwhelming.</span></div>
          <div className="trust-stat"><b>24/7</b><span>Available when questions come up</span></div>
          <div className="trust-stat"><b>3 ways</b><span>Type, upload, or record naturally</span></div>
          <div className="trust-stat"><b>1 place</b><span>For your ongoing consultation history</span></div>
        </section>
        <section className="health-process" id="process">
          <div className="process-intro"><span>How it works</span><h2>Care starts<br /><em>with a conversation.</em></h2><p>No complicated forms. Share what you know, and let AI Doctor help organize the next step.</p><button onClick={() => setView("dashboard")}>Begin your consultation <span>→</span></button></div>
          <div className="process-steps">
            <article><b>01</b><span className="step-icon">✎</span><h3>Tell us what&apos;s happening</h3><p>Describe symptoms or ask a question in your own words.</p></article>
            <article><b>02</b><span className="step-icon">⊙</span><h3>Add helpful context</h3><p>Upload an image or report, or record a voice note.</p></article>
            <article><b>03</b><span className="step-icon">✦</span><h3>Understand your results</h3><p>Receive a clear summary and keep it with your history.</p></article>
          </div>
        </section>
        <section className="health-quote">
          <span className="quote-mark">“</span>
          <blockquote>Technology should make healthcare feel more human — not more complicated.</blockquote>
          <div><span className="quote-avatar">✚</span><span><strong>The AI Doctor approach</strong><small>Clear information, with professional care always in mind.</small></span></div>
        </section>
        <section className="health-final-cta">
          <div><span>YOUR NEXT STEP STARTS HERE</span><h2>Make sense of<br /><em>your health story.</em></h2></div>
          <button onClick={() => setView("dashboard")}>Go to dashboard <span>↗</span></button>
        </section>
        <footer className="health-footer"><strong>AI Doctor</strong><span>Supports professional care. Does not replace it.</span><button onClick={() => setView("dashboard")}>Open consultation dashboard ↗</button></footer>
      </main>
    );
  }

  return (
    <main className="shell">
      <button className="back-home" onClick={() => setView("landing")}>← Back to home</button>
      <header><div><p className="eyebrow">AI DOCTOR / WEB PLATFORM</p><h1>Understand your health information.</h1><p className="muted">Upload a report, share an image, or record your symptoms. This tool supports—not replaces—professional medical care.</p></div><span className="badge">● Services online</span></header>
      <section className="grid">
        <aside className="card">
          <h2>Patient profile</h2>
          <form onSubmit={createPatient} className="stack">
            <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Patient name" required />
            <button type="submit">Create patient</button>
          </form>
          <div className="patient-list">{patients.map((item) => <button className="patient" key={item.id} onClick={() => loadHistory(item)}>{item.name}<span>View history</span></button>)}</div>
          {patient && <p className="selected">Selected: {patient.name}</p>}
        </aside>
        <section className="card">
          <h2>New consultation</h2>
          <form onSubmit={analyze} className="stack">
            <textarea value={symptoms} onChange={(event) => setSymptoms(event.target.value)} placeholder="Describe symptoms, report findings, or questions..." rows={7} />
            <input type="file" accept="image/*,.pdf" onChange={(event) => setImage(event.target.files?.[0] ?? null)} />
            <div className="record-row">
              <button type="button" className={recording ? "recording" : "secondary"} onClick={toggleRecording}>
                {recording ? "Stop recording" : "Record voice"}
              </button>
              {voice && <span className="file-chip">Voice ready</span>}
            </div>
            <button type="submit" disabled={busy || (!symptoms && !image && !voice)}>{busy ? "Analyzing..." : "Analyze securely"}</button>
          </form>
          {error && <p className="error">{error}</p>}
          {notice && <p className="notice">{notice}</p>}
          {transcript && <article className="transcript"><strong>Voice transcript</strong><p>{transcript}</p></article>}
          {analysis && <article className="result"><h2>Analysis</h2><pre>{analysis}</pre>{audioUrl && <div className="voice-output"><strong>Doctor's voice response</strong><audio controls src={audioUrl} /></div>}</article>}
        </section>
      </section>
      <section className="card history"><h2>Consultation history</h2>{history.length === 0 ? <p className="muted">Select a patient to view saved consultations.</p> : history.map((item) => <article className="history-item" key={item.id}><time>{new Date(item.createdAt).toLocaleString()}</time><p><strong>Input:</strong> {item.symptoms}</p><p><strong>Risk:</strong> {item.riskLevel || "Not specified"}</p><pre>{item.aiSummary || "No summary was saved."}</pre></article>)}</section>
    </main>
  );
}
