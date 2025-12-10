# Backend (FastAPI)

cd backend
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --port 8000
