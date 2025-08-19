from fastapi import FastAPI
from app.api.v1.routers.tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/api/v1")
