# ☕ Local Best Friend AI Companion (Café Dora)

An offline, 100% private, multilingual AI companion with internal English cognitive reasoning, local vector RAG, emotional intelligence, and an interactive 3D Three.js Artisanal Café UI.

---

## 🌟 Repository Overview

| Directory | Description |
|---|---|
| [`local_bestfriend_ai/`](./local_bestfriend_ai/) | Full companion backend, Unsloth QLoRA fine-tuning scripts, cognitive brain, local vector RAG, Ollama Modelfile, terminal CLI (`chat.py`), and FastAPI web server (`web_app.py`). |
| [`stitch_ui/`](./stitch_ui/) | Artisanal Café UI design specifications, interactive Three.js barista animation mockups, and visual design documentation. |

---

## ✨ Key Highlights

- **🧠 English Brain, Multilingual Heart**: Thinks step-by-step internally in English `<thought>` tags, then speaks naturally in English, Hinglish, Marathi, Marathish, or Hindi with zero corporate speak.
- **⚡ 8 Superpowers**: Chai & Chill wind-down (`/chill`), Vibe DJ music curator (`/vibe`), Roast-Me accountability coach (`/roast`), Wingman message doctor (`/wingman`), Hype-Man energy booster (`/hype`), Vision screen commentary (`/snap`), Life Diary stats (`/stats`), and thought inspection (`/thought`).
- **☕ 3D Interactive Café Experience**: Real-time Three.js coffee cup & barista avatar animations, ambient lo-fi soundscapes, and reactive mood themes.
- **🔒 100% Private & Offline**: All memories, goals, and vector embeddings are stored locally on your machine with no external telemetry.

---

## 🚀 Quick Start

See the detailed runbook and setup instructions in [`local_bestfriend_ai/README.md`](./local_bestfriend_ai/README.md).

```powershell
cd local_bestfriend_ai

# 1. Install dependencies
pip install -r requirements.txt

# 2. Vectorize local knowledge base
python train_rag.py

# 3. Launch interactive CLI companion
python chat.py

# 4. Or launch the 3D Web Companion (Port 7860)
python web_app.py
```

---

## 📄 License
MIT License
