"""Application-facing orchestration for image analysis and composition."""

from pathlib import Path

from PIL import Image

from .emotion import Mood, analyze_image, mood_from_name
from .music import generate_track


def compose(image: Image.Image, mood_name: str | None, duration: int, tempo: int, output_dir: Path) -> tuple[Mood, Path]:
	detected = analyze_image(image)
	mood = mood_from_name(mood_name) if mood_name else detected
	filename = f"{mood.name.lower()}_{tempo}bpm_{duration}s.wav"
	return mood, generate_track(mood, duration, tempo, output_dir / filename)
