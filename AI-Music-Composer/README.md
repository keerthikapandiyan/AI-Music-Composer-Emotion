# MUSE / AI Music Composer

MUSE turns an uploaded image into a short original WAV soundtrack. It estimates a broad mood from the image's brightness, saturation, and contrast, then generates a deterministic ambient melody.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Upload a JPG or PNG, choose `Auto-detect` or a mood direction, set the duration and pulse, and select **Generate soundtrack**. Generated WAV files are written to `data/generated_music/`.
