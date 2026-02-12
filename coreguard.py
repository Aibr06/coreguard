import sqlite3
import json
import time
from fastapi import FastAPI, Header, HTTPException # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from typing import List, Optional

DB_PATH = "coregaurd.db"
API_KEY = "dev-coregaurd-key"

app = FastAPI(title="CoreGaurd Server")

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS device_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            received_at INTEGER NOT NULL,
            payload TEXT NOT NULL
        );
        """)
        con.commit()

init_db()

class CheckResult(BaseModel):
    check_id: str
    status: str
    severity: str
    details: Optional[str] = None

class AgentPayload(BaseModel):
    device_id: str
    hostname: str
    os: str
    agent_version: str
    metrics: dict
    checks: List[CheckResult]

@app.post("/ingest")
def ingest(payload: AgentPayload, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        now = int(time.time())
        cur.execute(
            "INSERT INTO device_reports (device_id, received_at, payload) VALUES (?, ?, ?)",
            (payload.device_id, now, json.dumps(payload.dict()))
        )
        con.commit()
        rows = cur.execute("""
          SELECT device_id, MAX(received_at) as last_seen
          FROM device_reports
          GROUP BY device_id
          ORDER BY last_seen DESC
        """).fetchall()
    return [{"device_id": r[0], "last_seen": r[1]} for r in rows]