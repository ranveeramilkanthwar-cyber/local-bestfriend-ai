import os
import json
import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class MemoryManager:
    """
    Manages persistent local memory for the Best Friend AI:
    1. SQLite Life Diary (conversations, moods, goals)
    2. Inside Joke Vault (dynamic inside jokes & callbacks)
    3. Personal Fact RAG (preferences, habits, personal notes)
    """

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.data_dir / "diary.db"
        self.jokes_path = self.data_dir / "inside_jokes.json"
        self.notes_path = self.data_dir / "personal_notes.txt"

        self._init_sqlite()
        self._init_jokes()
        self._load_facts()

    def _init_sqlite(self):
        """Initializes SQLite schema for local privacy-first life diary."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_message TEXT,
                    assistant_response TEXT,
                    detected_language TEXT,
                    detected_mood TEXT,
                    thought_summary TEXT
                )
            """)
            # Daily Mood & Debrief table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_debriefs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    wins TEXT,
                    frustrations TEXT,
                    mood_rating TEXT,
                    summary TEXT
                )
            """)
            # Active Goals & Accountability table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    deadline TEXT,
                    goal_text TEXT,
                    status TEXT,
                    roast_count INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def _init_jokes(self):
        """Ensures the Inside Joke Vault exists."""
        if not self.jokes_path.exists():
            default_jokes = [
                {
                    "id": "joke_001",
                    "trigger": "database or prod or sql",
                    "joke_en": "Remember that time you almost pushed test credentials to production? Good times.",
                    "joke_hi": "Bhai kam se kam iss baar prod database drop mat karna jaise uss din kiya tha 😂",
                    "joke_mr": "Bhava, fakta production var test run nako karus, aapan gelya veli vaachlo hoto!"
                }
            ]
            with open(self.jokes_path, "w", encoding="utf-8") as f:
                json.dump(default_jokes, f, indent=2, ensure_ascii=False)

    def _load_facts(self):
        """Reads personal notes for factual retrieval."""
        self.facts: List[str] = []
        if self.notes_path.exists():
            try:
                with open(self.notes_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Split into bullet points or paragraphs
                lines = [l.strip("- ").strip() for l in content.split("\n") if l.strip() and not l.strip().startswith("[") and not l.strip().startswith("#")]
                self.facts = [l for l in lines if len(l) > 5]
            except Exception as e:
                print(f"[MemoryManager] Note load warning: {e}")

    def query_facts(self, query: str, top_k: int = 3) -> str:
        """
        Lightweight lexical & semantic fact retrieval without external heavy dependencies.
        Returns relevant personal facts to keep the model grounded.
        """
        if not self.facts:
            return ""

        query_words = set(query.lower().split())
        scored_facts = []
        for fact in self.facts:
            fact_words = set(fact.lower().split())
            overlap = len(query_words.intersection(fact_words))
            if overlap > 0:
                scored_facts.append((overlap, fact))

        scored_facts.sort(key=lambda x: x[0], reverse=True)
        top_matches = [f[1] for f in scored_facts[:top_k]]
        if top_matches:
            return "\n".join(f"- {m}" for m in top_matches)
        return ""

    def check_inside_jokes(self, query: str, language: str = "Hinglish") -> Optional[str]:
        """
        Checks if user message triggers an inside joke from the vault.
        """
        if not self.jokes_path.exists():
            return None

        try:
            with open(self.jokes_path, "r", encoding="utf-8") as f:
                jokes = json.load(f)

            query_lower = query.lower()
            for item in jokes:
                triggers = [t.strip() for t in item.get("trigger", "").split("or")]
                for trig in triggers:
                    if trig and trig in query_lower:
                        if "marathi" in language.lower():
                            return item.get("joke_mr") or item.get("joke_en")
                        elif "hindi" in language.lower() or "hinglish" in language.lower():
                            return item.get("joke_hi") or item.get("joke_en")
                        else:
                            return item.get("joke_en")
        except Exception:
            pass
        return None

    def add_inside_joke(self, trigger_keywords: str, joke_en: str, joke_hi: str = "", joke_mr: str = ""):
        """Dynamically stores a new inside joke."""
        jokes = []
        if self.jokes_path.exists():
            try:
                with open(self.jokes_path, "r", encoding="utf-8") as f:
                    jokes = json.load(f)
            except Exception:
                jokes = []

        new_entry = {
            "id": f"joke_{len(jokes) + 1:03d}",
            "trigger": trigger_keywords,
            "joke_en": joke_en,
            "joke_hi": joke_hi or joke_en,
            "joke_mr": joke_mr or joke_en
        }
        jokes.append(new_entry)
        with open(self.jokes_path, "w", encoding="utf-8") as f:
            json.dump(jokes, f, indent=2, ensure_ascii=False)

    def log_interaction(self, user_msg: str, assistant_reply: str, lang: str, mood: str, thought_summary: str):
        """Persists the turn to SQLite chat history."""
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO chat_history (timestamp, user_message, assistant_response, detected_language, detected_mood, thought_summary)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (now, user_msg, assistant_reply, lang, mood, thought_summary))
                conn.commit()
        except Exception as e:
            print(f"[MemoryManager] Log interaction error: {e}")

    def save_debrief(self, wins: str, frustrations: str, mood_rating: str, summary: str):
        """Stores evening Chai & Chill debrief in diary.db."""
        today = datetime.date.today().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO daily_debriefs (date, wins, frustrations, mood_rating, summary)
                VALUES (?, ?, ?, ?, ?)
            """, (today, wins, frustrations, mood_rating, summary))
            conn.commit()

    def add_goal(self, goal_text: str, deadline: str):
        """Adds an active accountability target."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO active_goals (created_at, deadline, goal_text, status)
                VALUES (?, ?, ?, 'PENDING')
            """, (now, deadline, goal_text))
            conn.commit()

    def get_stats_summary(self) -> Dict[str, Any]:
        """Calculates weekly stats and mood distribution for /stats dashboard."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_history")
            total_messages = cursor.fetchone()[0]

            cursor.execute("""
                SELECT detected_mood, COUNT(*) FROM chat_history 
                WHERE detected_mood IS NOT NULL AND detected_mood != ''
                GROUP BY detected_mood ORDER BY COUNT(*) DESC LIMIT 5
            """)
            top_moods = cursor.fetchall()

            cursor.execute("""
                SELECT detected_language, COUNT(*) FROM chat_history 
                GROUP BY detected_language ORDER BY COUNT(*) DESC
            """)
            languages = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) FROM active_goals WHERE status = 'PENDING'")
            pending_goals = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM daily_debriefs")
            total_debriefs = cursor.fetchone()[0]

        return {
            "total_messages": total_messages,
            "top_moods": top_moods,
            "languages": languages,
            "pending_goals": pending_goals,
            "total_debriefs": total_debriefs
        }
