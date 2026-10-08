import os, uuid
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/cpu")
def cpu_bound(n: int = Query(3_000_000, ge=1, le=500_000_000)):
    result = 0
    for i in range(n):
        result += i * i
    return {"type": "CPU-bound", "n": n}

@app.get("/memory")
def memory_task(size: int = Query(1500, ge=1, le=50_000)):
    matrix = [[1] * size for _ in range(size)]
    total = sum(sum(row) for row in matrix)
    return {"type": "memory-bound", "total": total}

@app.get("/io")
def io_bound(size: int = Query(20, ge=1, le=5000)):
    filename = f"/tmp/io_{uuid.uuid4().hex}.bin"
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
    return {"type": "I/O-bound", "operations": size}