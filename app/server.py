import os
import time
import uuid
import logging
from fastapi import FastAPI, Query

DATA_DIR = os.getenv("DATA_DIR", "/mnt/dados")
LOG_DIR = os.path.join(DATA_DIR, "logs")
IO_DIR = os.path.join(DATA_DIR, "io")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(IO_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("app")
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


@app.get("/memory")
def memory_task(size: int = Query(1500, ge=1, le=50_000)):
    log.info("GET /memory | início | size=%d", size)
    inicio = time.perf_counter()
    matrix = [[1] * size for _ in range(size)]
    total = sum(sum(row) for row in matrix)
    duracao = time.perf_counter() - inicio
    log.info("GET /memory | fim | size=%d | duração=%.3fs", size, duracao)
    return {"type": "memory-bound", "total": total}


@app.get("/io")
def io_bound(size: int = Query(20, ge=1, le=5000)):
    log.info("GET /io | início | size=%d", size)
    inicio = time.perf_counter()
    filename = os.path.join(IO_DIR, f"io_{uuid.uuid4().hex}.bin")
    data = os.urandom(1024 * 1024)
    try:
        for _ in range(size):
            with open(filename, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            with open(filename, "rb") as f:
                f.read()
    finally:
        if os.path.exists(filename):
            os.remove(filename)
    duracao = time.perf_counter() - inicio
    log.info("GET /io | fim | size=%d | duração=%.3fs", size, duracao)
    return {"type": "I/O-bound", "operations": size}