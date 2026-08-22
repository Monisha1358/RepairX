from fastapi import FastAPI

app = FastAPI(title="RepairX API")

@app.get("/")
def root():
    return {
        "name": "RepairX",
        "status": "online",
        "message": "RepairX backend is running"
    }