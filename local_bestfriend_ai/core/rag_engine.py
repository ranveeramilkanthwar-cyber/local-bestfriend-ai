import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

# Mask torchao if present to avoid PyTorch 2.6 inductor conflicts
sys.modules['torchao'] = None

class TransformerEmbedder:
    """
    Self-contained semantic vector embedder using HuggingFace transformers.
    Directly computes L2-normalized mean-pooled 384-dimensional embeddings
    without depending on datasets or pyarrow (100% AppLocker & Windows compliant).
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        # Move to CPU for small RAG queries to save GPU VRAM for the main LLM (Phi-3)
        self.model.to("cpu")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        import torch.nn.functional as F
        all_embeddings = []
        self.torch.set_grad_enabled(False)

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            encoded = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=256,
                return_tensors="pt"
            )
            encoded = {k: v.to("cpu") for k, v in encoded.items()}
            outputs = self.model(**encoded)

            # Mean pooling with attention mask
            mask = encoded["attention_mask"].unsqueeze(-1).expand(outputs[0].size()).float()
            sum_embeddings = self.torch.sum(outputs[0] * mask, 1)
            sum_mask = self.torch.clamp(mask.sum(1), min=1e-9)
            mean_pooled = sum_embeddings / sum_mask
            normalized = F.normalize(mean_pooled, p=2, dim=1)
            all_embeddings.append(normalized.numpy())

        return np.vstack(all_embeddings).astype(np.float32)


class LocalRAGEngine:
    """
    High-Performance Local RAG Engine:
    - 384-dimensional Dense Semantic Vector Space
    - Dual Index: Factual Knowledge Base + Extensive Conversational Dialogue Exemplars
    - Real-time continuous self-learning on chat interactions
    - Hybrid Semantic Cosine Similarity + Dialect alignment + Lexical keyword fallback
    """

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.data_dir = self.base_dir / "data"
        self.corpus_path = self.data_dir / "rag_corpus.json"
        self.notes_path = self.data_dir / "personal_notes.txt"
        self.conv_path = self.data_dir / "conversational_rag_dataset.json"
        self.cache_path = self.data_dir / "rag_vectors.npz"

        self.knowledge_docs: List[Dict[str, str]] = []
        self.dialogues: List[Dict[str, str]] = []

        self.knowledge_embeddings: Optional[np.ndarray] = None
        self.dialogue_embeddings: Optional[np.ndarray] = None

        self._embedder: Optional[TransformerEmbedder] = None

        self._load_corpus()
        self._init_embeddings()

    def _get_embedder(self) -> Optional[TransformerEmbedder]:
        """Lazy loader for TransformerEmbedder."""
        if self._embedder is None:
            try:
                self._embedder = TransformerEmbedder()
            except Exception as e:
                print(f"[RAG Engine] Notice: TransformerEmbedder init fallback: {e}")
                self._embedder = None
        return self._embedder

    def _load_corpus(self):
        """Loads factual documents, personal notes, and conversational pairs."""
        self.knowledge_docs = []
        self.dialogues = []

        # 1. Structured Knowledge Corpus
        if self.corpus_path.exists():
            try:
                with open(self.corpus_path, "r", encoding="utf-8") as f:
                    items = json.load(f)
                    for item in items:
                        self.knowledge_docs.append({
                            "title": f"[{item.get('category', 'Fact')}] {item.get('topic', '')}",
                            "text": item.get("content", ""),
                            "category": item.get("category", "Fact")
                        })
            except Exception as e:
                print(f"[RAG] Warning loading JSON corpus: {e}")

        # 2. Dynamic Personal Notes
        if self.notes_path.exists():
            try:
                with open(self.notes_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("- "):
                            self.knowledge_docs.append({
                                "title": "[Personal Fact]",
                                "text": line.lstrip("- ").strip(),
                                "category": "Personal Note"
                            })
            except Exception as e:
                print(f"[RAG] Warning loading personal notes: {e}")

        # 3. Conversational Message-Response Dataset
        if self.conv_path.exists():
            try:
                with open(self.conv_path, "r", encoding="utf-8") as f:
                    self.dialogues = json.load(f)
            except Exception as e:
                print(f"[RAG] Warning loading conversational dataset: {e}")

    @property
    def documents(self) -> List[Dict[str, str]]:
        """Combined list for backward compatibility."""
        combined = list(self.knowledge_docs)
        for d in self.dialogues:
            combined.append({
                "title": f"[{d.get('category', 'Chat')}] ({d.get('language', 'Hinglish')})",
                "text": f"User: {d.get('user', '')} | BestFriend: {d.get('assistant', '')}"
            })
        return combined

    def build_and_save_index(self):
        """
        Computes dense semantic embeddings for both factual knowledge and conversational dialogues.
        Saves precomputed vectors into data/rag_vectors.npz for sub-millisecond retrieval.
        """
        embedder = self._get_embedder()
        if not embedder:
            print("[RAG] Embedder unavailable; falling back to lexical indexing.")
            return

        print(f"[RAG] Vectorizing {len(self.knowledge_docs)} knowledge facts & {len(self.dialogues)} dialogues...")

        # 1. Knowledge vectors
        k_texts = [f"{d['title']}: {d['text']}" for d in self.knowledge_docs]
        if k_texts:
            self.knowledge_embeddings = embedder.encode(k_texts)
        else:
            self.knowledge_embeddings = np.empty((0, 384), dtype=np.float32)

        # 2. Dialogue vectors (embed user message + category for intent matching)
        d_texts = [f"{d.get('category', '')} {d.get('user', '')}" for d in self.dialogues]
        if d_texts:
            self.dialogue_embeddings = embedder.encode(d_texts)
        else:
            self.dialogue_embeddings = np.empty((0, 384), dtype=np.float32)

        # Save to disk
        np.savez_compressed(
            self.cache_path,
            knowledge=self.knowledge_embeddings,
            dialogue=self.dialogue_embeddings,
            k_count=len(self.knowledge_docs),
            d_count=len(self.dialogues)
        )
        print(f"[RAG] Successfully built and cached index at {self.cache_path}!")

    def _init_embeddings(self):
        """Loads cached index if available and valid; otherwise builds it."""
        if self.cache_path.exists():
            try:
                data = np.load(self.cache_path)
                k_emb = data["knowledge"]
                d_emb = data["dialogue"]
                k_count = int(data.get("k_count", len(k_emb)))
                d_count = int(data.get("d_count", len(d_emb)))

                if k_count == len(self.knowledge_docs) and d_count == len(self.dialogues):
                    self.knowledge_embeddings = k_emb
                    self.dialogue_embeddings = d_emb
                    return
            except Exception:
                pass
        # Cache miss or invalid -> rebuild
        self.build_and_save_index()

    def retrieve(self, query: str, top_k: int = 3, threshold: float = 0.35) -> str:
        """
        Retrieves top_k most relevant knowledge facts and personal memories using cosine similarity.
        """
        if not self.knowledge_docs:
            return ""

        embedder = self._get_embedder()
        if (
            embedder is not None
            and self.knowledge_embeddings is not None
            and len(self.knowledge_embeddings) == len(self.knowledge_docs)
        ):
            q_emb = embedder.encode([query])[0]
            scores = np.dot(self.knowledge_embeddings, q_emb)
            top_indices = np.argsort(scores)[::-1][:top_k]

            results = []
            for idx in top_indices:
                if scores[idx] >= threshold:
                    doc = self.knowledge_docs[idx]
                    results.append(f"- **{doc['title']}**: {doc['text']}")

            return "\n".join(results)

        # Lexical keyword fallback
        query_tokens = set(re.findall(r'\b\w+\b', query.lower()))
        scored = []
        for doc in self.knowledge_docs:
            doc_tokens = set(re.findall(r'\b\w+\b', (doc["title"] + " " + doc["text"]).lower()))
            overlap = len(query_tokens.intersection(doc_tokens))
            if overlap > 0:
                scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_k]
        return "\n".join([f"- **{d['title']}**: {d['text']}" for _, d in top])

    def retrieve_dialogue_exemplar(self, query: str, lang: str = "Hinglish") -> Optional[str]:
        """
        Finds the closest message-response pair matching user intent and target language.
        Uses 384-dimensional dense semantic vector similarity + language alignment bonus.
        Returns a formatted gold-standard few-shot exemplar for the prompt.
        """
        if not self.dialogues:
            return None

        embedder = self._get_embedder()
        lang_clean = lang.lower()

        if (
            embedder is not None
            and self.dialogue_embeddings is not None
            and len(self.dialogue_embeddings) == len(self.dialogues)
        ):
            q_emb = embedder.encode([query])[0]
            sim_scores = np.dot(self.dialogue_embeddings, q_emb)

            # Combined score: semantic similarity + language match weight
            final_scores = []
            for i, d in enumerate(self.dialogues):
                d_lang = d.get("language", "").lower()
                lang_match = 1.0 if (lang_clean in d_lang or d_lang in lang_clean) else 0.4
                combined_score = sim_scores[i] * 0.7 + (0.3 * lang_match)
                final_scores.append((combined_score, d))

            final_scores.sort(key=lambda x: x[0], reverse=True)
            best_score, best = final_scores[0]

            if best_score > 0.2:
                return (
                    f"[GOLD-STANDARD CONVERSATIONAL REFERENCE TO EMULATE EXACT TONE & SLANG]:\n"
                    f"User asked: '{best['user']}'\n"
                    f"Best Friend replied in {best['language']}: '{best['assistant']}'"
                )

        # Lexical fallback
        query_tokens = set(re.findall(r'\b\w+\b', query.lower()))
        scored = []
        for d in self.dialogues:
            d_lang = d.get("language", "").lower()
            d_text = (d.get("user", "") + " " + d.get("category", "")).lower()
            d_tokens = set(re.findall(r'\b\w+\b', d_text))

            overlap = len(query_tokens.intersection(d_tokens))
            if lang_clean in d_lang or d_lang in lang_clean:
                overlap += 2

            if overlap > 0:
                scored.append((overlap, d))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            best = scored[0][1]
            return (
                f"[GOLD-STANDARD CONVERSATIONAL REFERENCE TO EMULATE EXACT TONE & SLANG]:\n"
                f"User asked: '{best['user']}'\n"
                f"Best Friend replied in {best['language']}: '{best['assistant']}'"
            )

        return None

    def add_chat_interaction(self, user_msg: str, assistant_reply: str, lang: str, category: str = "Live Chat"):
        """
        Autonomous Continuous Self-Learning:
        Adds a real chat interaction directly into the RAG memory bank and vector space in real time!
        """
        if not user_msg or not assistant_reply:
            return

        new_item = {
            "category": category,
            "language": lang,
            "user": user_msg,
            "assistant": assistant_reply
        }
        self.dialogues.append(new_item)

        # Save to JSON
        try:
            with open(self.conv_path, "w", encoding="utf-8") as f:
                json.dump(self.dialogues, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[RAG] Warning saving new chat to dataset: {e}")

        # Vectorize new entry dynamically if embedder is ready
        embedder = self._get_embedder()
        if embedder and self.dialogue_embeddings is not None:
            try:
                new_vec = embedder.encode([f"{category} {user_msg}"])
                self.dialogue_embeddings = np.vstack([self.dialogue_embeddings, new_vec])
            except Exception as e:
                print(f"[RAG] Vector update error: {e}")
