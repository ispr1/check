# CHECK-360 Backend

FastAPI-based REST API for background verification platform.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run development server:
```bash
python -m src.main
```

API will be available at `http://localhost:8000`

## Folder Structure

