"""Procedural, dependency-light music generation."""

import math
import wave
from pathlib import Path

import numpy as np

from .emotion import Mood


SCALES = {
	"Joyful": [0, 2, 4, 7, 9, 12, 14, 16],
	"Calm": [0, 2, 3, 7, 9, 12, 14, 15],
	"Melancholic": [0, 2, 3, 5, 7, 8, 10, 12],
	"Dramatic": [0, 1, 3, 5, 7, 8, 10, 12],
}


def generate_track(mood: Mood, duration: int, tempo: int, output_path: Path, seed: int = 7) -> Path:
	"""Create a stereo ambient melody as a WAV file and return its path."""
	sample_rate = 22_050
	frame_count = sample_rate * duration
	rng = np.random.default_rng(seed)
	beat = 60.0 / tempo
	time = np.arange(frame_count, dtype=np.float32) / sample_rate
	scale = SCALES[mood.name]
	root = 220.0
	signal = np.zeros(frame_count, dtype=np.float32)

	for index, start in enumerate(np.arange(0, duration, beat)):
		start_frame = int(start * sample_rate)
		end_frame = min(frame_count, int((start + beat * 1.8) * sample_rate))
		if end_frame <= start_frame:
			continue
		note = scale[index % len(scale)] + (12 if index % 5 == 0 else 0)
		frequency = root * (2 ** (note / 12))
		local_time = time[start_frame:end_frame] - start
		envelope = np.minimum(local_time / 0.08, 1.0) * np.exp(-local_time / (beat * 1.35))
		signal[start_frame:end_frame] += 0.26 * np.sin(2 * math.pi * frequency * local_time) * envelope

	pad = 0.07 * np.sin(2 * math.pi * root * 0.5 * time)
	signal += pad + rng.normal(0, 0.003, frame_count).astype(np.float32)
	signal = np.tanh(signal * (1.0 + mood.energy * 0.65))
	stereo = np.column_stack((signal, np.roll(signal, int(sample_rate * 0.012))))
	pcm = (stereo * 32_000).astype(np.int16)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	with wave.open(str(output_path), "wb") as file:
		file.setnchannels(2)
		file.setsampwidth(2)
		file.setframerate(sample_rate)
		file.writeframes(pcm.tobytes())
	return output_path
