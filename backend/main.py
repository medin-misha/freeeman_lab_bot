from fastapi import FastAPI
import uvicorn
from api import main_router
from core import rmq_router

app = FastAPI()
app.include_router(main_router)
app.include_router(rmq_router)

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)