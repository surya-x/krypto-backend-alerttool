from fastapi import FastAPI
app = FastAPI()


@app.get("/alert/create", tags=['ROOT'])
def root() -> dict:
    return {"Ping": "Surya"}
