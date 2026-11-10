import os
import time
import logging
from fastapi import FastAPI, Query

DATA_DIR = os.getenv("DATA_DIR", "/data")
LOG_DIR = os.path.join(DATA_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "memory.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("memory")
log.info("Aplicação iniciada | DATA_DIR=%s", DATA_DIR)

app = FastAPI()


@app.get("/")
def root():
    log.info("GET / | status=online")
    return {"status": "online"}


@app.get("/memory")
def memory_task(size: int = Query(1500, ge=1, le=50_000)):
    log.info("GET /memory | início | size=%d", size)
    inicio = time.perf_counter()
    matrix = [[1] * size for _ in range(size)]
    total = sum(sum(row) for row in matrix)
    duracao = time.perf_counter() - inicio
    log.info("GET /memory | fim | size=%d | duração=%.3fs", size, duracao)
    return {"type": "memory-bound", "total": total}
