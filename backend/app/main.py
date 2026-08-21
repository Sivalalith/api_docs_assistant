from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.utils.rate_limiter import limiter

from app.api.upload import router as upload_router
from app.api.documents import router as documents_router
from app.api.query import router as query_router

app = FastAPI(title="API Documents Assistant", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://api-docs-assistant.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(query_router)

@app.get("/")
def root():
    return {
        "message": "API Documents Assistant Backend Running"
    }