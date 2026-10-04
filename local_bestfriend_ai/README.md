# 🤝 Local "Best Friend" AI Companion
### 100% Private, Local QLoRA Fine-Tuned Companion with English Cognitive Brain, Multilingual Heart, and Offline RAG

Built for **NVIDIA GeForce RTX 5050 (8GB VRAM)**, powered by **Unsloth (4-bit QLoRA)**, **Phi-3-mini-4k-instruct**, **Ollama (`q4_k_m.gguf`)**, and a **Local Vector RAG & SQLite Life Diary**.

---

## 🌟 Key Features

1. **🧠 English Brain, Multilingual Heart**:
   - The model reasons internally in high-logic English within hidden `<thought>` tags.
   - Responds in the **exact language and script you speak**:
     - **Texting Hinglish** (*"Arre bhai chill maar..."*)
     - **Texting Marathish** (*"Bhava kiti tension ghetoy..."*)
     - **Devanagari Hindi** (*"अरे भाई, टेंशन मत ले..."*)
     - **Devanagari Marathi** (*"अरे भावा, शांत राहा..."*)
     - **Indian English & Global English**
   - **Zero Corporate Speak**: Completely free of robotic phrases like *"As an AI..."* or *"I hope this helps"*.

2. **🎭 Adaptive 3-in-1 Persona (Unnamed by Default)**:
   - **Roast & Banter Mode**: Playful sarcasm, gaming camaraderie, witty teasing.
   - **Ride-or-Die Empathy Mode**: Deep listening, patient de-stressing, validating bad days.
   - **Tech Co-Pilot Mode**: Sharp code debugging, Git conflict rescue, architecture brainstorming.
   - Give it any nickname in chat using `/name <nickname>`.

3. **⚡ The 8 Companion Superpowers**:
   - `☕ /chill` - **Chai & Chill**: 3-step evening wind-down debrief that saves highlights to your private diary.
   - `🎵 /vibe <mood>` - **Vibe DJ**: Suggests curated YouTube/Spotify tracks (Hindi lo-fi, Marathi drill, phonk).
   - `🔥 /roast <goal>` - **Roast-Me Accountability**: Locks in a deadline and roasts you if you procrastinate.
   - `🎭 /wingman <draft>` - **Wingman Text Doctor**: Rewrites tricky messages into Casual, Diplomatic, and Direct styles.
   - `🚀 /hype [topic]` - **Instant Hype-Man**: High-energy confidence booster before gym PRs or interviews.
   - `📸 /snap` - **Vision Screen Peek**: Screen snapshot commentary via local Ollama vision.
   - `📊 /stats` - **Offline Life Diary**: Visual dashboard of conversation count, moods, and goals.
   - `🧠 /thought` - **Thought Toggle**: Show or hide the internal English reasoning loop.

---

## 📁 Workspace Directory Structure

```text
local_bestfriend_ai/
│
├── requirements.txt            # All pinned packages (torch, unsloth, ollama, rich, etc.)
├── check_env.py                # GPU & stack diagnostic tool
├── dataset.json                # 20+ rich multilingual multi-turn dialogues with <thought>
├── train.py                    # Unsloth 4-bit QLoRA fine-tuning & direct GGUF exporter
├── train_rag.py                # Vector indexing script for RAG knowledge base
├── Modelfile                   # Ollama model definition with cognitive English system prompt
│
├── core\
│   ├── __init__.py
│   ├── cognitive_brain.py      # Language/script detection, thought parser, prompt builder
│   ├── memory_manager.py       # SQLite Life Diary, Inside Joke Vault, fact lookup
│   ├── rag_engine.py           # SentenceTransformer vector embeddings & cosine search
│   ├── superpowers.py          # Chai & Chill, Vibe DJ, Wingman, Hype-Man, Accountability
│   └── vision_companion.py     # Desktop screen snapshot & vision reaction
│
├── data\
│   ├── personal_notes.txt      # Static reference facts & personal preferences
│   ├── rag_corpus.json         # Structured knowledge base for RAG
│   ├── inside_jokes.json       # Dynamic inside joke memory bank
│   ├── rag_vectors.npz         # Cached precomputed vector embeddings (sub-ms lookup)
│   └── diary.db                # SQLite database for daily logs & mood tracking
│
├── chat.py                     # Rich terminal interactive chat interface
└── README.md                   # Complete runbook & execution instructions
```

---

## 🚀 Step-by-Step Quickstart Runbook

### Step 1: Verify Hardware & Stack
Check that your GPU, CUDA, and fine-tuning packages are ready:
```powershell
python check_env.py
```

### Step 2: Index the RAG Knowledge Base
Train/vectorize your personal knowledge base into fast local embeddings:
```powershell
python train_rag.py
```

### Step 3: Fine-Tune with Unsloth (4-bit QLoRA) & Export GGUF
Run the automated QLoRA training script. Peak VRAM is only ~3.5GB on your RTX 5050:
```powershell
python train.py
```
*This produces `Phi-3-BestFriend/unsloth.Q4_K_M.gguf`.*

### Step 4: Register the Model in Ollama
Load the exported GGUF model into Ollama with the master system prompt:
```powershell
ollama create bestfriend -f Modelfile
```

*(Optional: You can test directly via Ollama CLI: `ollama run bestfriend`)*

### Step 5: Start the Interactive Terminal Companion Hub
Launch the rich terminal chat with full RAG, memory, and superpowers:
```powershell
python chat.py
```

### Step 6: Start the Modern Web Companion App (Live on Port 7860)
Launch the modern glassmorphic web interface with thought inspection, audio narration, and modals:
```powershell
python web_app.py
```
Open **[http://localhost:7860](http://localhost:7860)** in any browser.

---

## 🎮 Terminal Commands Inside `chat.py`

| Command | Action |
|---|---|
| `/chill` | Run the 3-minute evening wind-down debrief |
| `/vibe <mood>` | Get curated music recommendation with YouTube/Spotify links |
| `/roast <goal>` | Set an accountability target with a deadline |
| `/wingman <text>` | Rewrite awkward draft into Casual, Diplomatic, and Direct |
| `/hype [topic]` | Get an instant motivational boost in your native dialect |
| `/snap` | Take a screen capture and get best-friend commentary |
| `/stats` | View weekly mood distribution and conversation stats |
| `/thought` | Toggle visible English `<thought>` reasoning |
| `/rag` | Toggle RAG factual memory retrieval on/off |
| `/name <name>` | Change your companion's nickname anytime |
| `/help` | View help menu |
| `/exit` | Save and exit |

---

## 🔒 100% Offline & Private
All chats, diary entries, and personal notes are stored locally in `data/diary.db` and never leave your machine.
