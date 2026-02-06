cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Migraciones
alembic upgrade head

# Run
uvicorn <TU_MODULO>:app --reload --host 0.0.0.0 --port 8000
