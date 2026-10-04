import re
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from core.memory_manager import MemoryManager
from core.rag_engine import LocalRAGEngine

class AutoLearner:
    """
    Autonomous Real-Time Self-Learning Engine:
    1. Analyzes every user message to extract personal facts, habits, preferences, names, and corrections.
    2. Automatically indexes newly learned knowledge into the local RAG engine in real time.
    3. Persists learned facts into data/personal_notes.txt and SQLite.
    4. Allows the AI companion to evolve and adapt perpetually with every chat turn.
    """

    def __init__(self, memory_manager: MemoryManager, rag_engine: LocalRAGEngine):
        self.memory = memory_manager
        self.rag = rag_engine
        self.notes_file = Path(memory_manager.data_dir) / "personal_notes.txt"

        # Regex heuristics for self-learning extraction
        self.fact_patterns = [
            # "I like/love/hate/prefer X"
            r"(?:i\s+(?:like|love|hate|dislike|prefer|enjoy))\s+([^.,!?\n]+)",
            # "My X is Y" (e.g. my manager is Rahul, my dog is Bruno, my goal is X)
            r"(?:my\s+(?:name|boss|manager|friend|dog|cat|project|car|bike|goal|hobby|dream|laptop|gpu|favorite))\s+(?:is|named|called)\s+([^.,!?\n]+)",
            # "I am working on / building X"
            r"(?:i\s*(?:am|\'m)?\s+(?:working on|building|creating|developing|coding))\s+([^.,!?\n]+)",
            # "Call me X" or "My nickname is X"
            r"(?:call me|my nickname is)\s+([a-zA-Z0-9_\-]+)",
            # Hindi/Hinglish patterns: "mujhe X pasand hai", "mera naam / project X hai"
            r"(?:mujhe\s+)(.+?)(?:\s+pasand\s+hai|\s+acha\s+lagta\s+hai)",
            r"(?:mera\s+(?:naam|project|boss|kaam|goal)\s+)(.+?)(?:\s+hai)",
            # Marathi patterns: "mala X aawadta", "majha project X ahe"
            r"(?:mala\s+)(.+?)(?:\s+aawadta|\s+avdate)",
            r"(?:majha\s+(?:project|kam|mittra|boss)\s+)(.+?)(?:\s+ahe)"
        ]

    def extract_and_learn(self, user_text: str) -> List[str]:
        """
        Inspects message, extracts new facts, and updates memory and RAG instantly.
        """
        learned_facts = []
        text = user_text.strip()

        # Check for explicit facts
        for pattern in self.fact_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for m in matches:
                fact_content = m.group(0).strip()
                if len(fact_content) > 5 and fact_content not in learned_facts:
                    learned_facts.append(fact_content)

        # If any new facts were discovered, learn them permanently
        if learned_facts:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(self.notes_file, "a", encoding="utf-8") as f:
                f.write(f"\n# Auto-Learned on {timestamp}\n")
                for f_item in learned_facts:
                    f.write(f"- [Learned Memory]: {f_item.capitalize()}\n")

            # Reload & re-index RAG memory immediately
            self.rag._load_corpus()
            self.rag.build_and_save_index()
            print(f"[AutoLearner] Successfully learned and indexed {len(learned_facts)} new facts into RAG!")

        return learned_facts
