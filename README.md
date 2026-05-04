# 🩺 AI Doctor with Vision & Voice

### 🚀 Multimodal AI Healthcare Assistant (Voice + Vision + LLM)

<p align="center">
  <img src="https://img.shields.io/badge/AI-Multimodal-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Gradio-UI-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Whisper-STT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/TTS-gTTS%20%7C%20ElevenLabs-red?style=for-the-badge" />
</p>

---

## 🌟 Project Overview

AI Doctor with Vision & Voice is a next-generation AI-powered healthcare assistant that simulates basic medical consultation using both voice input and image analysis. The system combines speech recognition, computer vision, and large language models to provide a human-like interaction experience.

Users can describe their symptoms through voice and upload an image of the affected area. The system processes both inputs and generates a response in text as well as audio format.

---

## 🎯 Problem Statement

Access to healthcare is often delayed, expensive, or unavailable in remote areas. Most digital solutions lack multimodal capability and fail to understand real-world user conditions effectively.

This project solves these problems by providing:

* Instant AI-based response
* Low-cost solution
* Easy accessibility
* Multimodal understanding (Voice + Image)

---

## 🧠 System Workflow


flowchart TD
    A[User Voice Input 🎤] --> B[Speech-to-Text (Whisper)]
    C[User Image 🖼️] --> D[Vision Model]
    B --> E[Multimodal LLM]
    D --> E
    E --> F[AI Response]
    F --> G[Text Output]
    F --> H[Text-to-Speech 🔊]
```

---

## ✨ Features

* 🎙️ Real-time Voice Input
* 🧠 Speech-to-Text using Whisper
* 🖼️ Image Upload & Analysis
* 🤖 AI-generated medical suggestions
* 🔊 Voice Output using TTS
* 🌐 Interactive UI using Gradio
* ⚡ Fast inference using Groq

---

## 🏗️ Architecture

The system follows a modular layered architecture. The input layer handles user voice and image data, which is processed using speech recognition and computer vision models. The processed data is then sent to a multimodal large language model, which generates a response. Finally, the output layer converts the response into both text and speech.

---

## 🛠️ Tech Stack

### 👨‍💻 Programming Language

* Python

### 🧠 AI Models

* Whisper (Speech-to-Text)
* LLaMA Vision Model
* Groq API (LLM inference)

### 🔊 Audio

* gTTS
* ElevenLabs

### 🌐 Frameworks & Tools

* Gradio
* VS Code
* Git & GitHub

---

## 📂 Project Structure

```bash
AI-DOCTOR/
│
├── app.py / grad.py            # Main app
├── brain_of_doctor.py          # AI logic
├── voice_of_patient.py         # Speech-to-text
├── voice_of_doctor.py          # Text-to-speech
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/kushsahu767/AI-DOCTOR.git
cd AI-DOCTOR
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key_here
ELEVENLABS_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
python grad.py
```

Open in browser:

```
http://127.0.0.1:7860
```

---



## 📸 Usage

1. Record your voice describing symptoms
2. Upload an image (optional)
3. Submit input
4. View:

   * Transcribed text
   * AI-generated response
   * Audio output

---

## 📊 Results

The system successfully processes multimodal inputs and generates meaningful responses. It provides both text and voice output, making it highly interactive and user-friendly. The response time is fast, and the results are context-aware for basic healthcare assistance.

---

## ⚠️ Limitations

* Not a replacement for professional doctors
* Depends on input quality
* Requires internet connection

---

## 🚀 Future Scope

* Mobile application development
* Multi-language support
* Advanced disease detection
* Offline functionality
* Integration with wearable devices

---

## ⚠️ Disclaimer

This project is for educational purposes only.
It does not provide real medical diagnosis. Always consult a certified doctor.

---

## 👨‍💻 Author

Kush Sahu
UI/UX Designer | AI Developer

---

## 🏗️ Development Note

This project is independently designed and developed by me, including the system architecture, UI/UX design, and integration of all modules such as voice processing, image analysis, and response generation.

AI technologies like Whisper, LLMs, and Text-to-Speech have been used strictly as functional tools for processing and debugging purposes. The complete logic, design, and implementation of this system are developed by me.

---

## 🤝 Contributing

* Fork the repository
* Create a new branch
* Submit a pull request

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share it

---

