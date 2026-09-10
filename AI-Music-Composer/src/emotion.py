"""Lightweight visual mood estimation used by the music pipeline."""

from dataclasses import dataclass

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class Mood:
	name: str
	energy: float
	brightness: float
	warmth: float
	description: str


MOODS = {
	"Joyful": Mood("Joyful", 0.82, 0.86, 0.78, "bright, warm, and optimistic"),
	"Calm": Mood("Calm", 0.28, 0.68, 0.50, "soft, spacious, and reflective"),
	"Melancholic": Mood("Melancholic", 0.34, 0.32, 0.35, "tender, cinematic, and introspective"),
	"Dramatic": Mood("Dramatic", 0.76, 0.40, 0.42, "bold, tense, and cinematic"),
}


def analyze_image(image: Image.Image) -> Mood:
	"""Estimate a broad musical mood from average image color and contrast."""
	rgb = np.asarray(image.convert("RGB").resize((64, 64)), dtype=np.float32) / 255.0
	brightness = float(np.mean(rgb))
	saturation = float(np.mean(np.max(rgb, axis=2) - np.min(rgb, axis=2)))
	contrast = float(np.std(rgb))

	if brightness > 0.68 and saturation > 0.22:
		return MOODS["Joyful"]
	if brightness < 0.38 and contrast > 0.20:
		return MOODS["Dramatic"]
	if brightness < 0.48:
		return MOODS["Melancholic"]
	return MOODS["Calm"]


def mood_from_name(name: str) -> Mood:
	"""Return a known mood, falling back to Calm for invalid input."""
	return MOODS.get(name, MOODS["Calm"])
