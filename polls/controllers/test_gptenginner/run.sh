pip install -r requirements.txt
uvicorn app.app:app --host 0.0.0.0 --port 8000 &
pytest tests/
