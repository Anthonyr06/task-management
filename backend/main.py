from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.db import Base, engine
from src.models import (
    user,
    project,
    task,
    task_assignee,
    comment,
    webhook,
    refresh_token,
)

from src.api.routes.auth import router as auth_router
from src.api.routes.projects import router as projects_router
from src.api.routes.tasks import router as tasks_router
from src.api.routes.comments import router as comments_router
from src.api.routes.webhooks import router as webhooks_router
from src.api.routes.users import router as users_router
from src.core.logging import setup_logging
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.users import router as users_router


from src.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MRevolution Backend API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(webhooks_router)
app.include_router(users_router)
app.include_router(users_router)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/_webhook-test")
def webhook_test(payload: dict):
    print("WEBHOOK RECEIVED:", payload)
    return {"ok": True}
