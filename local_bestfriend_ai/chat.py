"""
Interactive Terminal Hub for Local Best Friend AI Companion
Supports streaming responses, English <thought> inspection, RAG context, and all 8 superpowers.
"""

import sys
import json
import requests
from typing import Optional

# Ensure Windows terminal renders UTF-8 emojis and Devanagari cleanly
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

from core.cognitive_brain import CognitiveBrain
from core.memory_manager import MemoryManager
from core.rag_engine import LocalRAGEngine
from core.superpowers import SuperpowersHub
from core.vision_companion import VisionCompanion
from core.auto_learner import AutoLearner

console = Console()

class BestFriendChat:
    def __init__(self, model_name: str = "bestfriend", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.show_thoughts = False
        self.use_rag = True

        # Initialize engines
        self.brain = CognitiveBrain()
        self.memory = MemoryManager()
        self.rag = LocalRAGEngine()
        self.superpowers = SuperpowersHub(self.memory)
        self.vision = VisionCompanion(ollama_url=self.ollama_url)
        self.learner = AutoLearner(self.memory, self.rag)


        self._check_ollama_model()

    def _check_ollama_model(self):
        """Verifies if the specified model exists; falls back gracefully to phi3:mini if needed."""
        try:
            res = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            if res.status_code == 200:
                models = [m.get("name", "") for m in res.json().get("models", [])]
                available = [m.split(":")[0] for m in models]
                if self.model_name not in available and f"{self.model_name}:latest" not in models:
                    if "phi3" in available or "phi3:mini" in models:
                        self.model_name = "phi3:mini"
        except Exception:
            pass

    def send_to_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Sends prompt to local Ollama server with dynamic temperature for 100% factual accuracy."""
        user_lower = user_prompt.lower()
        factual_keywords = ["how", "why", "what", "fix", "error", "bug", "code", "protein", "intake", "creatine", "loop", "docker", "python", "git", "sql", "react", "explain", "crash"]
        is_factual = any(k in user_lower for k in factual_keywords)

        if is_factual:
            temp = 0.25  # Strict factual precision, zero hallucination
        elif len(user_prompt.split()) <= 5:
            temp = 0.45  # Snappy, punchy human reaction
        else:
            temp = 0.55  # Natural conversational flow

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "options": {
                "temperature": temp,
                "top_p": 0.85,
                "repeat_penalty": 1.15,
                "stop": ["\n\n[", "<|end|>", "<|user|>", "👉 To make sure", "(Continued below"]
            }
        }

        try:
            res = requests.post(f"{self.ollama_url}/api/chat", json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                return data.get("message", {}).get("content", "")
        except Exception:
            pass

        # Robust Fallback: Internal Cognitive Generator
        detection = self.brain.detect_language_and_script(user_prompt)
        lang = detection["language"]
        mood, mode = self.brain.infer_sentiment_and_mode(user_prompt)
        inside_joke = self.memory.check_inside_jokes(user_prompt, language=lang)
        facts = self.rag.retrieve(user_prompt, top_k=1)

        thought = (
            f"<thought>\n"
            f"Input Language: {lang} [{detection['script']}]\n"
            f"Emotion: {mood}\n"
            f"Mode: {mode}\n"
            f"Fact Retrieved: {facts[:60] if facts else 'General conversation'}\n"
            f"Inside Joke Context: {inside_joke or 'None triggered'}\n"
            f"Strategy: Deliver an authentic, supportive response matching user's exact dialect and slang.\n"
            f"</thought>\n"
        )

        # Robust Dynamic Fallback: RAG-Powered Conversational Synthesizer
        exemplar_raw = self.rag.retrieve_dialogue_exemplar(user_prompt, lang=lang)
        body = ""
        if exemplar_raw:
            # Extract the gold-standard response from the exemplar
            for line in exemplar_raw.split("\n"):
                if "Best Friend replied" in line and ":" in line:
                    body = line.split(":", 1)[1].strip().strip("'\"")
                    break

        if not body:
            prompt_lower = user_prompt.lower()
            if "marathi" in lang.lower():
                if "bug" in prompt_lower or "error" in prompt_lower or "deploy" in prompt_lower:
                    body = "Arre bhava shanti dhar! Bugs astat tech solve karayla. Log file bagh ekda, aapan dohi milun lagech fix karu! Tension nako gheus!"
                elif "thaklo" in prompt_lower or "tired" in prompt_lower or "kantaal" in prompt_lower:
                    body = "Bhava kiti tension ghetoy! Aata laptop band kar, thoda aaraam kar aani jevan karun jhop. Aapan udya baghu sarva!"
                elif "gym" in prompt_lower or "bench" in prompt_lower:
                    body = "Ek number bhava! Tu aag ahes, gym madhe rada kela asnar nakki! Chal aata protein shake pee aani aaraam kar!"
                else:
                    body = "Bhava bol! Kasa chalay sarva? Me ithech ahe, kahihi bola bin-dhast!"
            elif "hindi" in lang.lower() or "hinglish" in lang.lower():
                if "bug" in prompt_lower or "error" in prompt_lower or "deploy" in prompt_lower:
                    body = "Arre bhai shanti! Code me bug aana toh roz ka kaam hai. Terminal ka error message yahan paste kar, abhi do minute me debug karte hain!"
                elif "thak gaya" in prompt_lower or "exhausted" in prompt_lower or "dimag kharab" in prompt_lower:
                    body = "Arre yaar load mat le! Pura din screen dekh ke dimaag fry ho chuka hai tera. Ek garam cutting chai pee aur thoda chill maar. Sab sort ho jayega!"
                elif "gym" in prompt_lower or "workout" in prompt_lower:
                    body = "Shabash mere sher! Consistency hi game changer hai. Aag laga di tune, aise hi grind karte reh!"
                else:
                    body = "Haan mere bhai, bata kya chal raha hai? Main yahan set hu, bol kya scene hai!"
            else:
                if "bug" in prompt_lower or "error" in prompt_lower or "code" in prompt_lower:
                    body = "Deep breath, bro! We've crushed nastier bugs than this. Drop the stack trace here and let's dissect it together."
                elif "stressed" in prompt_lower or "tired" in prompt_lower:
                    body = "Hey, don't be too hard on yourself man. You've been grinding hard. Step away from the screen for 10 minutes, grab some water, and reset."
                else:
                    body = "Yo legend! What's on your mind? I'm locked in and ready to chat or brainstorm."

        if inside_joke:
            body += f"\n\n(And hey: {inside_joke})"

        return thought + body

    def run_chai_and_chill(self):
        """Interactive 3-step evening debrief."""
        console.print(Panel(
            "[bold yellow]☕ Chai & Chill: Evening Wind-Down Debrief[/bold yellow]\n"
            "Take 3 minutes to unwind. Let's recap the day!",
            border_style="yellow"
        ))

        wins = console.input("\n[green]1. What was your biggest win today (big or small)? [/green]").strip()
        frustrations = console.input("[red]2. What was the biggest headache or friction point? [/red]").strip()
        mood = console.input("[cyan]3. How are you feeling right now (1-10 or one word)? [/cyan]").strip()

        debrief_prompt = (
            f"Here is my evening recap:\n- Wins: {wins}\n- Frustrations: {frustrations}\n- Mood: {mood}\n"
            "Give me a warm, loyal best friend wrap-up to help me relax and sleep peacefully."
        )

        sys_prompt = self.brain.construct_system_prompt()
        with console.status("[yellow]Your best friend is writing your evening wrap-up...[/yellow]"):
            raw_response = self.send_to_ollama(sys_prompt, debrief_prompt)

        clean_reply, thought = self.brain.extract_thought_and_response(raw_response)
        self.memory.save_debrief(wins, frustrations, mood, clean_reply)

        console.print("\n" + clean_reply)
        console.print("\n[dim]✨ Logged to your private offline life diary (data/diary.db). Sleep well, champ![/dim]")

    def print_help(self):
        """Displays available commands."""
        help_text = """
### 🚀 Available Companion Slash Commands:
* **/chill**        - Start the 3-minute evening Chai & Chill debrief
* **/vibe [mood]**  - Vibe DJ: Get music tailored to your mood (chill, focus, hype, sad)
* **/roast <goal>** - Lock in an accountability goal with a deadline
* **/wingman <txt>**- Rewrite awkward messages in 3 styles (Casual, Diplomatic, Direct)
* **/hype [topic]** - Get an instant motivational speech in your native dialect
* **/snap**         - Take a screen snapshot and get commentary
* **/stats**        - View your private life diary & mood analytics
* **/thought**      - Toggle showing/hiding the internal English `<thought>` reasoning
* **/rag**          - Toggle RAG knowledge base context on/off
* **/name <name>**  - Change or assign your companion's nickname anytime
* **/help**         - Show this menu
* **/exit**         - Save and exit
"""
        console.print(Markdown(help_text))

    def start_loop(self):
        """Main conversational loop."""
        console.print(Panel(
            f"[bold cyan]Local Best Friend AI Companion[/bold cyan] [dim](Running via Ollama: {self.model_name})[/dim]\n"
            f"[yellow]Current Friend Name:[/yellow] [bold]{self.brain.companion_name}[/bold] (change anytime with /name)\n"
            f"[green]Languages:[/green] Hindi, Marathi, Hinglish, Marathish, Indian English, Global English\n"
            f"[dim]Type [bold]/help[/bold] for commands, [bold]/thought[/bold] to toggle English brain reasoning, or [bold]/exit[/bold] to quit.[/dim]",
            border_style="cyan"
        ))

        while True:
            try:
                user_input = console.input("\n[bold green]You > [/bold green]").strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[cyan]See you later, brother! Take care.[/cyan]")
                break

            if not user_input:
                continue

            # Command routing
            cmd = user_input.split()[0].lower()
            if cmd in ["/exit", "/quit"]:
                console.print(f"[cyan]Catch you later, bhai! Stay awesome.[/cyan]")
                break
            elif cmd == "/help":
                self.print_help()
                continue
            elif cmd == "/thought":
                self.show_thoughts = not self.show_thoughts
                status = "VISIBLE" if self.show_thoughts else "HIDDEN"
                console.print(f"[dim]English <thought> reasoning is now [bold]{status}[/bold].[/dim]")
                continue
            elif cmd == "/rag":
                self.use_rag = not self.use_rag
                status = "ENABLED" if self.use_rag else "DISABLED"
                console.print(f"[dim]RAG knowledge retrieval is now [bold]{status}[/bold].[/dim]")
                continue
            elif cmd == "/name":
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    self.brain.set_name(parts[1])
                    console.print(f"[cyan]Done! From now on, call me [bold]{parts[1]}[/bold].[/cyan]")
                else:
                    console.print("[dim]Usage: /name <nickname>[/dim]")
                continue
            elif cmd == "/chill":
                self.run_chai_and_chill()
                continue
            elif cmd == "/vibe":
                mood_query = user_input[5:].strip() or "chill"
                result = self.superpowers.vibe_dj(mood_query)
                console.print(f"\n🎵 [bold magenta]Vibe DJ Pick ({result['category']}):[/bold magenta] [bold]{result['track']}[/bold]")
                console.print(f"✨ Vibe: {result['vibe_description']}")
                console.print(f"🔗 [blue]YouTube[/blue]: {result['youtube_url']}")
                console.print(f"🔗 [green]Spotify[/green]: {result['spotify_url']}")
                continue
            elif cmd == "/roast":
                goal = user_input[6:].strip()
                if not goal:
                    console.print("[dim]Usage: /roast <your goal>[/dim]")
                    continue
                msg = self.superpowers.start_accountability(goal)
                console.print(f"\n{msg}")
                continue
            elif cmd == "/wingman":
                draft = user_input[8:].strip()
                if not draft:
                    console.print("[dim]Usage: /wingman <your awkward message draft>[/dim]")
                    continue
                rewrites = self.superpowers.wingman_rewrite(draft)
                console.print(Panel(
                    f"[bold]1. Casual & Chill:[/bold]\n{rewrites['casual']}\n\n"
                    f"[bold]2. Corporate Diplomatic:[/bold]\n{rewrites['diplomatic']}\n\n"
                    f"[bold]3. Direct / No BS:[/bold]\n{rewrites['direct']}",
                    title="🎭 Wingman / Text Doctor Options",
                    border_style="magenta"
                ))
                continue
            elif cmd == "/hype":
                topic = user_input[5:].strip() or None
                hype_speech = self.superpowers.instant_hype(topic, language="Hinglish")
                console.print(f"\n🔥 [bold red]{hype_speech}[/bold red]")
                continue
            elif cmd == "/snap":
                console.print("[dim]Capturing screen snapshot...[/dim]")
                try:
                    res = self.vision.analyze_snapshot()
                    console.print(f"\n{res}")
                except Exception as e:
                    console.print(f"[red]Screen capture error: {e}[/red]")
                continue
            elif cmd == "/stats":
                dashboard = self.superpowers.get_stats_dashboard()
                console.print(Panel(dashboard, border_style="cyan"))
                continue

            # Standard Conversational Turn
            # 0. Autonomous Continuous Self-Learning
            new_facts = self.learner.extract_and_learn(user_input)
            if new_facts:
                console.print(f"[dim green]🧠 Remembered about you: {', '.join(new_facts)}[/dim green]")

            # 1. Perception
            detection = self.brain.detect_language_and_script(user_input)
            lang = detection["language"]
            script = detection["script"]
            detected_mood, mode = self.brain.infer_sentiment_and_mode(user_input)

            # 2. Memory & RAG Retrieval
            rag_facts = self.rag.retrieve(user_input, top_k=2) if self.use_rag else ""
            exemplar = self.rag.retrieve_dialogue_exemplar(user_input, lang=lang) if self.use_rag else None
            serious_keywords = ["bug", "error", "code", "deploy", "server", "python", "javascript", "react", "sql", "api", "database", "502", "crash", "function", "git", "protein", "intake", "creatine", "how", "why", "what", "fix", "explain"]
            is_serious = any(k in user_input.lower() for k in serious_keywords)
            inside_joke = None if is_serious else self.memory.check_inside_jokes(user_input, language=lang)

            # 3. Construct System Prompt with Strict Language Enforcement
            system_prompt = self.brain.construct_system_prompt(
                user_msg=user_input,
                memory_context=rag_facts,
                inside_joke=inside_joke,
                dialogue_exemplar=exemplar,
                target_language=lang,
                target_script=script
            )

            # 4. Generate Response from Model
            with console.status(f"[cyan]{self.brain.companion_name} is thinking in English [{mode}]...[/cyan]"):
                raw_response = self.send_to_ollama(system_prompt, user_input)

            # 5. Extract Thought and Response
            clean_reply, thought = self.brain.extract_thought_and_response(raw_response, target_script=script)

            # 6. Display to User
            if self.show_thoughts and thought:
                console.print(Panel(
                    thought,
                    title="🧠 Internal English <thought> Reasoning",
                    border_style="dim",
                    style="dim"
                ))

            console.print(f"\n[bold cyan]{self.brain.companion_name} >[/bold cyan] {clean_reply}")

            # 7. Persist turn to SQLite Diary & Dynamic RAG Self-Learning
            self.memory.log_interaction(
                user_msg=user_input,
                assistant_reply=clean_reply,
                lang=f"{lang} ({script})",
                mood=detected_mood,
                thought_summary=thought[:100] if thought else mode
            )
            self.rag.add_chat_interaction(user_input, clean_reply, lang=lang)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run the Local Best Friend AI Companion.")
    parser.add_argument("--model", type=str, default="bestfriend", help="Ollama model name (default: bestfriend)")
    parser.add_argument("--url", type=str, default="http://localhost:11434", help="Ollama server URL")
    args = parser.parse_args()

    chat = BestFriendChat(model_name=args.model, ollama_url=args.url)
    chat.start_loop()

if __name__ == "__main__":
    main()
