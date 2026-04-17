from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from api import main_router
from core import rmq_router
from service.health import collect_health_report

app = FastAPI()
app.include_router(main_router)
app.include_router(rmq_router)

Instrumentator().instrument(app).expose(app)


@app.get("/live")
async def live():
    return {"status": "ok", "service": "backend"}


@app.get("/ready")
async def ready(response: Response):
    report = await collect_health_report()
    if not report.is_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "fail"}

    return {"status": "ok"}


@app.get("/health")
async def health(response: Response):
    report = await collect_health_report()
    if not report.is_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return report.as_dict()


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
