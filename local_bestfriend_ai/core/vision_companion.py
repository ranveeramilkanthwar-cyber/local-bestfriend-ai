import os
import base64
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class VisionCompanion:
    """
    Multimodal Screen & Vision Companion:
    - Captures desktop screen / active window snapshot
    - Connects to local Ollama vision models (e.g., moondream, llava, or minicpm-v)
    - Delivers casual, best-friend commentary on memes, outfits, bugs, or game screens
    """

    def __init__(self, base_dir: Optional[str] = None, ollama_url: str = "http://localhost:11434"):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.snap_path = self.data_dir / "latest_snap.png"
        self.ollama_url = ollama_url

    def capture_screen(self) -> Path:
        """Takes a full screen capture and saves it locally."""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(self.snap_path, "PNG")
            return self.snap_path
        except Exception as e:
            print(f"[VisionCompanion] Capture error: {e}")
            raise

    def analyze_snapshot(self, user_prompt: str = "Look at this screenshot, what do you think?", model: str = "moondream") -> str:
        """
        Sends the captured image to local Ollama vision model.
        Falls back with friendly guidance if vision model is not installed.
        """
        try:
            self.capture_screen()
        except Exception as e:
            return f"📸 Screen snapshot capture error: {e}"

        with open(self.snap_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

        payload = {
            "model": model,
            "prompt": f"You are a close best friend. React casually to what you see on my screen. User asked: '{user_prompt}'",
            "images": [encoded_image],
            "stream": False
        }

        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Yo, I checked it out, looks interesting!")
            else:
                return (
                    f"📸 Snapshot saved to [cyan]{self.snap_path}[/cyan]!\n"
                    f"(Note: To get live vision commentary, make sure you have a vision model in Ollama like `ollama pull moondream` or `ollama pull llava`)."
                )
        except Exception:
            return (
                f"📸 Snapshot captured and saved to [cyan]{self.snap_path}[/cyan]!\n"
                "(Ollama local vision service is offline or busy right now. Run `ollama pull moondream` to enable auto-reactions)."
            )
