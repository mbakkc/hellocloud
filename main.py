import asyncio
import json
import time

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import psutil

app = FastAPI()

@app.get("/")
async def index():
    with open("templates/index.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)

async def generate_stats():
    prev = psutil.net_io_counters()
    prev_time = time.time()
    while True:
        await asyncio.sleep(1)
        current = psutil.net_io_counters()
        current_time = time.time()
        delta_sent = current.bytes_sent - prev.bytes_sent
        delta_recv = current.bytes_recv - prev.bytes_recv
        elapsed = current_time - prev_time
        speed_sent = delta_sent / elapsed
        speed_recv = delta_recv / elapsed
        data = json.dumps({"sent": speed_sent, "recv": speed_recv})
        yield f"data: {data}\n\n"
        prev = current
        prev_time = current_time

@app.get("/stats")
async def stats():
    return StreamingResponse(generate_stats(), media_type="text/event-stream")
