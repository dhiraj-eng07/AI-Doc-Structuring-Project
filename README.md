# AI Doc Structuring Project

Minimal project skeleton that extracts text from PDFs, processes it with an AI/LLM step (stubbed), and writes structured JSON -> Excel.

Files:
- `requirements.txt` - Python deps
- `.env.example` - env/example keys
- `src/` - core modules: `extract.py`, `ai_processor.py`, `excel_writer.py`, `utils.py`
- `app/streamlit_app.py` - small demo UI
- `sample_runs/` - sample outputs and placeholder `Output.xlsx`

Run locally (demo):

1. Create a virtualenv and install requirements:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the Streamlit demo:
```
streamlit run app/streamlit_app.py
```

Note: The AI step is a stub returning sample structured output. Replace `src/ai_processor.py` internals with your preferred LLM integration.
