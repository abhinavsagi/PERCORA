# PECORA Full-Stack v3 — Multi-page frontend

This version makes every top navigation option functional.

### Pages
- Home
- Market Analysis
- Decision Simulator
- Journal
- Learn
- About

### Run
```bat
python -m pip install -r requirements.txt
python -m uvicorn backend:app --host 127.0.0.1 --port 8000
```

In a second terminal:
```bat
python -m streamlit run app.py
```

The frontend still works without the backend for the local simulator. The backend is used by Analyze My Decision.
Live market data is intentionally not connected yet.
