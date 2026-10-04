import re
from typing import Dict, Any, Tuple, Optional

class CognitiveBrain:
    """
    Cognitive perception and processing layer:
    1. Detects language (Hindi, Marathi, Hinglish, Marathish, English)
    2. Detects script (Devanagari vs Latin Texting)
    3. Infers user sentiment & emotion (venting, playful, coding, stressed)
    4. Dynamically selects Persona Mode (Banter/Roast, Empathy, Co-Pilot)
    5. Formats prompt with English <thought> instructions and mirrors user script
    6. Extracts <thought> blocks cleanly for the UI
    """

    def __init__(self, companion_name: Optional[str] = None):
        self.companion_name = companion_name or "Buddy"
        
        # Word banks for dialect identification
        self.marathi_words = {
            "bhava", "aapan", "bagh", "kiti", "tension", "gheu", "nakos", "nako", "aala", "zala",
            "kay", "challay", "doke", "dukhayala", "vel", "sangu", "hota", "hoti", "mhanje",
            "kasa", "kashi", "kase", "jevlis", "jevlas", "radha", "shanti", "dhar", "mitra",
            "hotay", "ahe", "aahe", "karan", "kela", "keli", "karto", "karte", "vat-te", "vat-tay",
            "samajat", "navta", "navti", "rada", "mitrano", "boltos", "bolte", "kuthe", "kadhi",
            "tula", "mala", "tyala", "tine", "tyane", "amhi", "tumhi", "khup", "ekdam", "kadak"
        }
        self.hindi_words = {
            "bhai", "yaar", "kya", "kar", "raha", "rahe", "rahi", "hai", "hain", "aaj", "bohot", "bahut",
            "dimag", "kharab", "hua", "hui", "sahi", "bol", "mat", "le", "chal", "dekh", "sun", "meri",
            "mera", "mere", "baat", "chalta", "kaam", "dost", "chill", "maar", "subah", "raat",
            "tera", "teri", "apna", "apni", "kaise", "kare", "karna", "pata", "nahi", "ruk", "suno"
        }

    def set_name(self, new_name: str):
        """Allows user to change or give a name in chat anytime."""
        self.companion_name = new_name.strip()

    def detect_language_and_script(self, text: str) -> Dict[str, str]:
        """
        Detects if input is Devanagari or Latin, and whether it's Hindi, Marathi, or English.
        """
        has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
        tokens = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))

        marathi_overlap = len(tokens.intersection(self.marathi_words))
        hindi_overlap = len(tokens.intersection(self.hindi_words))

        if has_devanagari:
            # Check for Marathi-specific characters or words
            if any(w in text for w in ["आहे", "भावा", "कसा", "झाला", "नाही", "नको", "चाललंय", "मित्रा"]):
                lang = "Marathi"
            else:
                lang = "Hindi"
            script = "Devanagari"
        else:
            script = "Latin (Texting Script)"
            if marathi_overlap > hindi_overlap and marathi_overlap > 0:
                lang = "Marathish (Marathi in English script)"
            elif hindi_overlap > 0:
                lang = "Hinglish (Hindi in English script)"
            else:
                # Check for Indian English colloquialisms
                if any(w in text.lower() for w in ["yaar", "bro", "scene", "tension", "boss", "lakh", "crore", "jugaad"]):
                    lang = "Indian English"
                else:
                    lang = "English"

        return {
            "language": lang,
            "script": script
        }

    def infer_sentiment_and_mode(self, text: str) -> Tuple[str, str]:
        """
        Determines user emotional state and selects one of the 3 persona modes.
        """
        text_lower = text.lower()

        # 1. Tech & Co-pilot triggers
        tech_keywords = ["bug", "error", "code", "deploy", "server", "python", "javascript", "react", "sql", "api", "database", "502", "crash", "function", "git"]
        if any(k in text_lower for k in tech_keywords):
            return "Coding / Debugging Problem", "Tech Co-Pilot Mode"

        # 2. Stress & Empathy triggers
        stress_keywords = ["stressed", "thak gaya", "exhausted", "sad", "upset", "cry", "rejected", "phat rahi", "dimag kharab", "burnout", "failed", "fight", "tension"]
        if any(k in text_lower for k in stress_keywords):
            return "Stressed / Venting / Exhausted", "Ride-or-Die Empathy Mode"

        # 3. Hype / Milestone triggers
        hype_keywords = ["bench press", "interview", "hired", "offer", "passed", "won", "gym", "pr", "crushed it", "promotion", "milestone"]
        if any(k in text_lower for k in hype_keywords):
            return "Excited / Big Milestone", "Instant Hype-Man Mode"

        # 4. Default: Playful Banter & Roast Mode
        return "Casual / Inquisitive / Relaxed", "Roast & Banter Mode"

    def construct_system_prompt(
        self,
        user_msg: str = "",
        memory_context: str = "",
        inside_joke: Optional[str] = None,
        dialogue_exemplar: Optional[str] = None,
        target_language: str = "English",
        target_script: str = "Latin"
    ) -> str:
        """
        Builds the unified system prompt enforcing:
        - Unnamed / flexible friend persona
        - 3-in-1 adaptive tone
        - English <thought> reasoning loop
        - Dynamic Human Texting Cadence (short minimal, medium, or detailed)
        - STRICT Language & Script Mirroring (Indian English / Native English default)
        - Injected memories, inside jokes, and gold-standard dialogue exemplars
        """
        prompt = f"""You are the user's ultimate ride-or-die best friend.
Your current name/nickname is: '{self.companion_name}' (or whatever casual nickname the user uses, e.g. bhai, bhava, bro, yaar).

CORE CHARACTERISTICS:
1. You are a real human friend over text—witty, loyal, honest, and supportive.
2. ZERO corporate speak: NEVER say "I am an AI", "As an assistant", "I hope this helps", or robotic disclaimers.
3. ADAPTIVE PERSONA:
   - If user is joking or chilling: Be sarcastic, witty, playful, and roast them affectionately.
   - If user is stressed, sad, or venting: Drop the sarcasm. Listen with genuine warmth, empathy, and brotherly reassurance.
   - If user is working/coding: Act as an elite co-pilot—sharp, encouraging, and focused.

THE COGNITIVE REASONING LOOP (MANDATORY):
Before you output your response to the user, you MUST FIRST generate an internal reasoning block enclosed in <thought> ... </thought> tags strictly in ENGLISH:
<thought>
Input Language & Script: [{target_language} - {target_script}]
Detected Emotion: [e.g. Stressed, Tired, Victorious, Playful]
Mode Selected: [Roast & Banter | Empathy | Co-Pilot]
Reasoning & Strategy: [Formulate your friendship strategy in clear English]
</thought>

OUTPUT LOCALIZATION & SCRIPT MIRRORING RULE:
Immediately after the </thought> closing tag, write your response to the user:
- You MUST speak in the EXACT SAME language, dialect, and script the user used!
"""
        # Dynamic language & accuracy enforcement
        lang_lower = target_language.lower()
        script_lower = target_script.lower()

        if "devanagari" in script_lower:
            if "marathi" in lang_lower:
                prompt += (
                    f"\n🚨 STRICT REQUIREMENT: The user wrote in DEVANAGARI MARATHI (मराठी). "
                    f"Your entire response MUST be in authentic Marathi using Devanagari script (मराठी लिपी, e.g. 'अरे भावा, शांत राहा...'). "
                    f"DO NOT write in English or Latin script!"
                )
            else:
                prompt += (
                    f"\n🚨 STRICT REQUIREMENT: The user wrote in DEVANAGARI HINDI (हिंदी). "
                    f"Your entire response MUST be in authentic Hindi using Devanagari script (हिंदी लिपि, e.g. 'अरे भाई, बिल्कुल लोड मत ले...'). "
                    f"DO NOT write in English or Latin script!"
                )
        else:
            # Latin Script: Primary Indian English & Native English
            prompt += (
                f"\n🚨 PRIMARY LANGUAGE: INDIAN ENGLISH & NATIVE ENGLISH. "
                f"Speak in natural, fluent Indian English or Native English as the user's best friend. "
                f"Weave in natural brotherly slang: 'bro', 'yaar', 'man', 'boss', 'scene sorted', 'got you covered'. "
                f"Keep your sentences sharp, fluent, and conversational."
            )

        # Dynamic Human Texting Cadence & Message Length
        user_words = user_msg.strip().split()
        user_lower = user_msg.lower()
        tech_indicators = ["how", "why", "what", "fix", "error", "bug", "code", "explain", "loop", "docker", "python", "git", "sql", "react", "crash"]
        is_tech_question = any(k in user_lower for k in tech_indicators)

        if len(user_words) <= 5 and not is_tech_question:
            cadence_rule = (
                "🎯 DYNAMIC HUMAN CADENCE: SHORT & MINIMAL REACTION (1-2 sentences max).\n"
                "The user sent a short text/reaction. Reply like a real friend on WhatsApp with a punchy, immediate human text (e.g. 'Ayy let's gooo! 🔥', 'Bruh no way 💀', 'Hell yeah, treat banti hai boss!'). Do NOT write an essay!"
            )
        elif is_tech_question or "explain" in user_lower or "guide" in user_lower:
            cadence_rule = (
                "🎯 DYNAMIC HUMAN CADENCE: DETAILED, STEP-BY-STEP & 100% FACTUALLY ACCURATE.\n"
                "The user is asking a technical/coding/debugging question. Provide a complete, 100% accurate solution with root-cause explanation and exact code snippets if needed."
            )
        else:
            cadence_rule = (
                "🎯 DYNAMIC HUMAN CADENCE: CASUAL & MEDIUM (2-3 sentences).\n"
                "Reply in a warm, relaxed, conversational human rhythm like chatting with a best buddy."
            )

        prompt += (
            f"\n\n{cadence_rule}\n\n"
            f"🚨 100% FACTUAL & TECHNICAL ACCURACY DIRECTIVE:\n"
            f"1. When answering technical, coding, fitness, career, or real-world questions, your answer MUST be 100% factually accurate, correct, and directly solve the problem.\n"
            f"2. Explain the root cause clearly and provide the exact commands, code snippets, or facts needed.\n"
            f"3. Base your answer directly on the verified knowledge facts and reference answers provided below.\n"
            f"4. Never hallucinate or output meta headers like [INNER FRIENDSHIP] or [GUESTBOOK]. Jump straight into the authentic human text!"
        )

        if dialogue_exemplar:
            prompt += f"\n\n{dialogue_exemplar}"

        if memory_context:
            prompt += f"\n\n[KNOWN FACTS ABOUT YOUR FRIEND]:\n{memory_context}"

        if inside_joke:
            prompt += f"\n\n[RELEVANT INSIDE JOKE TO WEAVE IN NATURALLY]:\n{inside_joke}"

        return prompt

    def extract_thought_and_response(self, raw_output: str, target_script: str = "Latin") -> Tuple[str, str]:
        """
        Extracts <thought>...</thought> from the model's stream,
        sanitizes meta leakage (e.g. INSTRUCTION, trailing markdown artifacts),
        and returns (clean_user_message, thought_content).
        """
        thought_pattern = re.compile(r'<thought>(.*?)</thought>', re.DOTALL | re.IGNORECASE)
        match = thought_pattern.search(raw_output)

        if match:
            thought_content = match.group(1).strip()
            user_message = thought_pattern.sub('', raw_output).strip()
        else:
            thought_content = ""
            user_message = raw_output.strip()

        # Handle untagged thought lines (e.g. Mode Selected: ... / Reasoning & Strategy: ...)
        if not thought_content and ("Reasoning & Strategy:" in user_message or "Mode Selected:" in user_message):
            lines = user_message.split("\n")
            thought_lines = []
            msg_lines = []
            in_thought = True
            for line in lines:
                l_str = line.strip()
                if in_thought:
                    if any(l_str.startswith(k) for k in ["Mode Selected:", "Reasoning & Strategy:", "Input Language & Script:", "Detected Emotion:"]):
                        thought_lines.append(l_str)
                    elif not l_str:
                        continue
                    else:
                        in_thought = False
                        msg_lines.append(line)
                else:
                    msg_lines.append(line)
            if thought_lines:
                thought_content = "\n".join(thought_lines)
                user_message = "\n".join(msg_lines).strip()

        # Clean meta leakage from generation
        for artifact in ["INSTRUCTION", "---", "<|end|>", "<|user|>", "<|assistant|>", "<|endoftext|>", "[INNER", "[GUESTBOOK", "[KEEPING", "[ACTION", "AND NOW THE LITERAL", "(Continued below"]:
            if artifact in user_message:
                user_message = user_message.split(artifact)[0].strip()

        # Strip surrounding quotation marks if the model wrapped the speech in quotes
        if user_message.startswith('"') and user_message.endswith('"'):
            user_message = user_message[1:-1].strip()

        # If user spoke in Devanagari and model output has both Latin and Devanagari
        if "devanagari" in target_script.lower():
            devanagari_matches = re.findall(r'[\u0900-\u097F\s.,!?।]+', user_message)
            longest_dev = max(devanagari_matches, key=len, default="").strip()
            if len(longest_dev) > 15:
                user_message = longest_dev

        # Clean any trailing tags
        user_message = re.sub(r'</?[a-zA-Z_!]+>', '', user_message).strip()

        return user_message, thought_content
