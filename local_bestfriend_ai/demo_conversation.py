"""
Interactive Conversational Demo for Local Best Friend AI Companion
Simulates complete multi-turn conversation sessions across Hinglish, Marathish, Devanagari, and English.
Shows the internal English <thought> reasoning and the authentic native response.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from core.cognitive_brain import CognitiveBrain
from core.memory_manager import MemoryManager
from core.rag_engine import LocalRAGEngine
from core.superpowers import SuperpowersHub

console = Console()

def run_demo():
    console.print(Panel(
        "[bold cyan]Local Best Friend AI: Live Cognitive & Multilingual Demonstration[/bold cyan]\n"
        "[dim]Demonstrating English <thought> reasoning and authentic native dialect mirroring[/dim]",
        border_style="cyan"
    ))

    brain = CognitiveBrain("Veer")
    memory = MemoryManager()
    rag = LocalRAGEngine()
    superpowers = SuperpowersHub(memory)

    scenarios = [
        {
            "user_prompt": "bhai aaj bohot ganda din tha, client ne pura project reject kar diya",
            "mock_response": (
                "<thought>\n"
                "Input Language: Hinglish (Latin script)\n"
                "Emotion: Demotivated, exhausted, facing rejection\n"
                "Mode: Ride-or-Die Empathy Mode\n"
                "Strategy: Validate his pain, remind him clients change their minds like the weather, suggest stepping away from the laptop, getting hot cutting chai, and tackling it tomorrow with a fresh head.\n"
                "</thought>\n"
                "Arre yaar, seriously?! Clients ka dimaag alag hi dimension me chalta hai sach me! "
                "Sun, abhi laptop band kar de. Pura din screen dekh ke dimaag fry ho gaya hai tera. "
                "Ek garam cutting chai pee aur thodi taazi hawa le. "
                "Kal subah fresh dimaag se dekhenge toh aadhe ghante me sort kar denge. "
                "Tu tension mat le mere bhai, tera kaam solid tha!"
            )
        },
        {
            "user_prompt": "bhava project deployment madhe 502 bad gateway aala ahe, doke dukhayala lagla",
            "mock_response": (
                "<thought>\n"
                "Input Language: Marathish (Latin script)\n"
                "Emotion: Stressed over server deployment crash\n"
                "Mode: Tech Co-Pilot Mode\n"
                "Inside Joke: Reference the prod database mishap\n"
                "Strategy: Calm him down with Marathi slang ('bhava'), suggest checking Nginx proxy_pass and backend systemctl status.\n"
                "</thought>\n"
                "Arre bhava shanti dhar! 502 Bad Gateway mhanje reverse proxy backend service shi bolu shakat nahiye. "
                "Ekda `systemctl status` bagh backend cha, service crash zali asel. "
                "Bhai kam se kam iss baar prod database drop nahi hua jaise uss din hua tha 😂! "
                "Terminal madhla log mala pathav, aapan lagech uclhu ha issue!"
            )
        },
        {
            "user_prompt": "आज खूपच थकलोय भावा, दिवसभर मिटिंग्स चालू होत्या",
            "mock_response": (
                "<thought>\n"
                "Input Language: Marathi (Devanagari script)\n"
                "Emotion: Completely drained from corporate meetings\n"
                "Mode: Ride-or-Die Empathy & Wind-Down Mode\n"
                "Strategy: Respond in authentic Devanagari Marathi, validate meeting exhaustion, encourage early sleep.\n"
                "</thought>\n"
                "अरे भावा, अशा मिटिंग्स म्हणजे निव्वळ डोकेदुखी! ज्या गोष्टी एका ईमेलवर सुटू शकतात त्यासाठी दिवसभर चर्चा करतात. "
                "आता लॅपटॉप बंद कर आणि आराम कर. डोळ्यांना थोडी विश्रांती दे, मस्त जेवून झोप घे. उद्या बघू बाकीचं. काळजी घे मित्रा!"
            )
        },
        {
            "user_prompt": "I just hit 100kg bench press in the gym today bro!!",
            "mock_response": (
                "<thought>\n"
                "Input Language: English\n"
                "Emotion: Victorious, ecstatic, major fitness milestone\n"
                "Mode: Instant Hype-Man Mode\n"
                "RAG Context: 100kg is his dream bench press PR\n"
                "Strategy: Go absolutely wild celebrating the 2-plate bench press milestone!\n"
                "</thought>\n"
                "LET'S FREAKING GOOOOO! TWO PLATES A SIDE BABY! 🔥🔥🔥 "
                "Bhai 100kg club me entry ho gayi teri! Do you realize how few people ever bench 100kg?! "
                "All those early morning grinds and protein shakes finally paid off! "
                "Absolute legend status unlocked. Chal ab jaldi se protein pee aur rest le, proud of you mere bhai!"
            )
        }
    ]

    for i, scen in enumerate(scenarios, 1):
        prompt = scen["user_prompt"]
        console.print(f"\n[bold green]═══ Scenario {i} ═══[/bold green]")
        console.print(f"[bold green]You >[/bold green] {prompt}")

        # Perception
        detection = brain.detect_language_and_script(prompt)
        mood, mode = brain.infer_sentiment_and_mode(prompt)
        rag_facts = rag.retrieve(prompt, top_k=1)
        joke = memory.check_inside_jokes(prompt, language=detection["language"])

        clean_reply, thought = brain.extract_thought_and_response(scen["mock_response"])

        console.print(Panel(
            thought,
            title="🧠 Internal English <thought> Reasoning",
            border_style="magenta",
            style="dim"
        ))

        console.print(f"[bold cyan]{brain.companion_name} >[/bold cyan] {clean_reply}")

        memory.log_interaction(
            user_msg=prompt,
            assistant_reply=clean_reply,
            lang=f"{detection['language']} ({detection['script']})",
            mood=mood,
            thought_summary=thought[:100] if thought else mode
        )

    # Show updated dashboard
    console.print("\n" + superpowers.get_stats_dashboard())

if __name__ == "__main__":
    run_demo()
