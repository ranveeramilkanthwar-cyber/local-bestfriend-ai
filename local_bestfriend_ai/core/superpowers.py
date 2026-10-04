import random
import datetime
from typing import Dict, Any, List, Optional
from core.memory_manager import MemoryManager

class SuperpowersHub:
    """
    Houses the companion's 8 special abilities:
    1. Chai & Chill Evening Debrief (/chill)
    2. Vibe DJ Mood-to-Music Matcher (/vibe)
    3. Roast-Me Accountability Partner (/roast)
    4. Wingman / Text Doctor (/wingman)
    5. Instant Hype-Man (/hype)
    6. Life Diary & Mood Analytics (/stats)
    """

    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        
        # Curated Vibe DJ Database
        self.music_catalog = {
            "chill": [
                {"title": "Prateek Kuhad / Anuv Jain Lofi Mix", "vibe": "Acoustic Hindi Indie", "search": "Anuv Jain Prateek Kuhad chill acoustic lofi"},
                {"title": "Midnight Chai Lofi Beats", "vibe": "Late-night Coding Instrumental", "search": "Hindi lofi beats to code relax chill to"},
                {"title": "Arijit Singh Unplugged Midnight Session", "vibe": "Soulful Nostalgia", "search": "Arijit Singh acoustic unplugged slow lofi"}
            ],
            "focus": [
                {"title": "Synthwave / Cyberpunk Deep Work", "vibe": "Zero Vocals Flow State", "search": "Synthwave radio chill synth for coding"},
                {"title": "Khruangbin / Instrumental Grooves", "vibe": "Smooth Psychedelic Chill", "search": "Khruangbin full live session instrumental"}
            ],
            "hype": [
                {"title": "Marathi Drill & Hip Hop Mix (Divine / Sambhaji)", "vibe": "Aggressive Street Energy", "search": "Marathi drill hip hop hype workout mix"},
                {"title": "Gym Phonk & High BPM Beats", "vibe": "Heavy PR Energy", "search": "Aggressive drift phonk workout motivation"}
            ],
            "sad": [
                {"title": "Late Night Soul & Rain Acoustic", "vibe": "Gentle Comfort", "search": "Late night acoustic hindi rain lofi mix"},
                {"title": "Cigarettes After Sex / Slowed Indie", "vibe": "Melancholic Calm", "search": "Cigarettes after sex slowed reverb chill"}
            ]
        }

    def vibe_dj(self, query_or_mood: str) -> Dict[str, Any]:
        """Recommends music matching the current vibe."""
        q = query_or_mood.lower()
        if any(w in q for w in ["gym", "workout", "hype", "energy", "pr", "lift"]):
            category = "hype"
        elif any(w in q for w in ["focus", "code", "work", "study", "deep"]):
            category = "focus"
        elif any(w in q for w in ["sad", "vent", "low", "upset", "cry"]):
            category = "sad"
        else:
            category = "chill"

        tracks = self.music_catalog.get(category, self.music_catalog["chill"])
        picked = random.choice(tracks)

        yt_link = f"https://www.youtube.com/results?search_query={picked['search'].replace(' ', '+')}"
        spotify_link = f"https://open.spotify.com/search/{picked['search'].replace(' ', '%20')}"

        return {
            "category": category.capitalize(),
            "track": picked["title"],
            "vibe_description": picked["vibe"],
            "youtube_url": yt_link,
            "spotify_url": spotify_link
        }

    def wingman_rewrite(self, draft_text: str) -> Dict[str, str]:
        """
        Transforms awkward or tricky drafts into 3 distinct styles:
        1. Casual & Chill
        2. Corporate Diplomatic
        3. Direct / No BS
        """
        # Provides instant structural blueprints for prompt injection or direct fallback
        return {
            "casual": f"Hey, wanted to quickly check in—{draft_text.lower().strip('.')} Let me know what you think!",
            "diplomatic": f"Hi there, regarding our recent discussion: {draft_text.strip()} I'd appreciate your perspective on this when you have a moment.",
            "direct": f"{draft_text.strip()} Bottom line: let's align on next steps today."
        }

    def instant_hype(self, topic: Optional[str] = None, language: str = "Hinglish") -> str:
        """Generates an explosive motivational speech in your native dialect."""
        t = f" about {topic}" if topic else ""
        if "marathi" in language.lower():
            return (
                f"Bhava aik! {t.capitalize() if t else 'Konala sangu nako'}, tu aag ahes! "
                "Tula shanka ghenyachi kahich garaj nahiye. "
                "Aapan kiti hard problems solve kele ahet te aathav! "
                "Fakta jaa aani radha karun taak! Koni tula rokhanar nahi, go smash it!"
            )
        elif "hindi" in language.lower() or "hinglish" in language.lower():
            return (
                f"Sun meri baat mere bhai! {t if t else 'Apne upar doubt karna band kar'}. "
                "Tu champion hai aur tune hamesha mushkil situation me deliver kiya hai! "
                "Imposter syndrome ko dustbin me phenk aur full confidence ke saath aage badh. "
                "Duniya ki aisi ki taisi, tu aag laga dega! Let's goooo!"
            )
        else:
            return (
                f"Listen to me, legend! Stop second-guessing yourself{t}. "
                "You've conquered harder things than this with your eyes closed. "
                "Lock in, walk into the room with absolute confidence, and claim your win. You got this!"
            )

    def start_accountability(self, goal: str, deadline_minutes: int = 60) -> str:
        """Registers a goal and returns an accountability pact message."""
        deadline_time = datetime.datetime.now() + datetime.timedelta(minutes=deadline_minutes)
        deadline_str = deadline_time.strftime("%I:%M %p")
        self.memory.add_goal(goal, deadline_str)
        return (
            f"🎯 Pact Locked! Goal: '{goal}'.\n"
            f"⏰ Deadline: {deadline_str} ({deadline_minutes} mins from now).\n"
            "If you're caught scrolling reels or slacking before then, expect zero mercy and full roasts! Get to work!"
        )

    def get_stats_dashboard(self) -> str:
        """Builds a formatted summary of private mood and conversation stats."""
        stats = self.memory.get_stats_summary()
        
        report = []
        report.append("📊 [bold cyan]Local Best Friend AI: Private Life & Mood Dashboard[/bold cyan]")
        report.append(f"• Total Conversations Logged: {stats['total_messages']}")
        report.append(f"• Evening Debriefs Completed: {stats['total_debriefs']}")
        report.append(f"• Active Goals in Progress   : {stats['pending_goals']}")

        report.append("\n🎭 [bold yellow]Top Detected Moods:[/bold yellow]")
        if stats['top_moods']:
            for mood, count in stats['top_moods']:
                report.append(f"  - {mood}: {count} times")
        else:
            report.append("  - Still gathering mood data—keep chatting!")

        report.append("\n🗣️ [bold green]Languages Used:[/bold green]")
        if stats['languages']:
            for lang, count in stats['languages']:
                report.append(f"  - {lang}: {count} turns")
        else:
            report.append("  - Standard English / Hinglish")

        report.append("\n🔒 [dim]100% Private: All data stored exclusively in local SQLite database (data/diary.db).[/dim]")
        return "\n".join(report)
