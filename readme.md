# 🧠 Video Keyframe and Audio Embedding Pipeline

This project provides a full pipeline to:

- Extract keyframes from a video
- Embed those frames using the CLIP model
- Transcribe audio using OpenAI Whisper
- Embed the transcribed audio using OpenAI Embeddings API

---

## 📦 Features

- ✅ Extracts frames at fixed time intervals from any video
- ✅ Embeds image frames using HuggingFace `CLIP`
- ✅ Transcribes audio tracks using OpenAI `whisper`
- ✅ Embeds resulting transcript text using OpenAI's `text-embedding-3-small`
- 🧪 Optional: Upload frame data to S3 (placeholder)

---

## 🛠️ Tech Stack

- `Python 3.11.9`
- `Whisper` (OpenAI)
- `Transformers` (CLIP from Hugging Face)
- `Torch` for tensor operations
- `OpenAI SDK` (>= 1.0)
- `PIL`, `cv2` for image handling
- `dotenv` for secure key management

---

## 📂 Project Structure

---

## ⚙️ Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd video_embedding_process
pyenv local 3.11.9
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your .env file

```bash
OPENAI_API_KEY=your_openai_key
```

### ▶️ Run the pipeline

```bash
python src/main.py
```

You’ll be prompted:

```bash
>video y/n?
>audio y/n?
```

Select y to process the video and/or transcribe + embed audio

###  ✏️ Notes

- Whisper models available: "tiny", "base", "small", "medium", "large", "turbo" (if using OpenAI hosted)
- Frame extraction interval and input paths are defined in constants.py
- GPU acceleration is supported with Whisper + Torch

### 📌 Future Improvements

- Upload to AWS S3 or other cloud storage
- Store embeddings in a vector database (like Pinecone or Weaviate)
- Parallelize frame and audio processing for speed
