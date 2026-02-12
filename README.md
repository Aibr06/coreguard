cat > README.md << 'EOF'
# CoreGuard

CoreGuard is a lightweight FastAPI ingestion backend for endpoint monitoring and security posture reporting.

## Features
- POST /ingest endpoint
- Pydantic validation for payload structure
- API key auth via X-API-Key header
- Stores reports in SQLite (device_id, timestamp, full payload)

## Run locally
Install:
```bash
pip install fastapi uvicorn pydantic
uvicorn coreguard:app --reload --port 8000

Then commit + push:

```bash
git add README.md
git commit -m "Add README"
git push
