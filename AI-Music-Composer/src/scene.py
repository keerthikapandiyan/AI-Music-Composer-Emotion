"""Small presentation helpers shared by the Streamlit scene."""

from pathlib import Path


def output_directory(project_root: Path) -> Path:
	return project_root / "data" / "generated_music"
