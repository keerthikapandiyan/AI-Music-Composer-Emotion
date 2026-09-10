from pathlib import Path

import streamlit as st
from PIL import Image

from src.emotion import MOODS
from src.pipeline import compose
from src.scene import output_directory


PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="MUSE / AI Music Composer", page_icon="M", layout="wide")
st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
	:root { --ink:#18231f; --paper:#f5f1e8; --lime:#c7e86a; --rust:#d9653d; }
	.stApp { background: var(--paper); color: var(--ink); }
	[data-testid="stHeader"] { background: transparent; }
	h1, h2, h3, p, label, button { font-family: 'Space Grotesk', sans-serif !important; }
	h1 { font-size: clamp(2.8rem, 7vw, 6.4rem) !important; line-height: .9 !important; letter-spacing: -0.06em !important; }
	.eyebrow { font: 500 0.76rem 'DM Mono', monospace; letter-spacing: .13em; text-transform: uppercase; color: var(--rust); }
	.lede { max-width: 34rem; font-size: 1.12rem; line-height: 1.45; }
	.panel { border-top: 2px solid var(--ink); padding-top: 1rem; margin-top: 1.5rem; }
	.mood { background: var(--lime); padding: 1rem 1.2rem; font: 600 1.3rem 'Space Grotesk', sans-serif; }
	.stButton > button { background: var(--ink); color: var(--paper); border: 0; border-radius: 0; min-height: 3.2rem; font-weight: 600; }
	.stDownloadButton > button { border-radius: 0; border: 2px solid var(--ink); }
	</style>
	""",
	unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">MUSE / 001 &nbsp; VISUAL TO SOUND</div>', unsafe_allow_html=True)
st.title("Compose the\natmosphere.")
st.markdown('<p class="lede">Drop in an image. MUSE reads its light, color, and tension, then shapes a small original soundtrack around the feeling.</p>', unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85], gap="large")
with left:
	st.markdown('<div class="panel"><div class="eyebrow">01 / SOURCE IMAGE</div></div>', unsafe_allow_html=True)
	upload = st.file_uploader("Upload a JPG or PNG", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
	if upload:
		image = Image.open(upload)
		st.image(image, use_container_width=True)
	else:
		st.info("Your image becomes the score's emotional starting point.")

with right:
	st.markdown('<div class="panel"><div class="eyebrow">02 / COMPOSITION</div></div>', unsafe_allow_html=True)
	mood_name = st.selectbox("Mood direction", ["Auto-detect"] + list(MOODS))
	duration = st.slider("Duration", min_value=8, max_value=45, value=16, step=1, format="%d sec")
	tempo = st.slider("Pulse", min_value=60, max_value=140, value=92, step=1, format="%d BPM")
	st.caption("Auto-detect uses the image's average light, saturation, and contrast.")
	compose_button = st.button("Generate soundtrack", use_container_width=True, type="primary")

if compose_button:
	if not upload:
		st.warning("Add an image before generating a soundtrack.")
	else:
		with st.spinner("Listening to the image..."):
			mood, track = compose(image, None if mood_name == "Auto-detect" else mood_name, duration, tempo, output_directory(PROJECT_ROOT))
		st.markdown(f'<div class="mood">{mood.name} / {mood.description}</div>', unsafe_allow_html=True)
		st.audio(track.read_bytes(), format="audio/wav")
		st.download_button("Download WAV", track.read_bytes(), file_name=track.name, mime="audio/wav")
