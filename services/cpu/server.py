import os
import time
import logging
from fastapi import FastAPI, Query

DATA_DIR = os.getenv("DATA_DIR", "/data")
LOG_DIR = os.path.join(DATA_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "cpu.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("cpu")
log.info("Aplicação iniciada | DATA_DIR=%s", DATA_DIR)

app = FastAPI()


@app.get("/")
def root():
    log.info("GET / | status=online")
    return {"status": "online"}


@app.get("/cpu")
def cpu_bound(n: int = Query(3_000_000, ge=1, le=500_000_000)):
    log.info("GET /cpu | início | n=%d", n)
    inicio = time.perf_counter()
    result = 0
    for i in range(n):
        result += i * i
    duracao = time.perf_counter() - inicio
    log.info("GET /cpu | fim | n=%d | duração=%.3fs", n, duracao)
    return {"type": "CPU-bound", "n": n}
