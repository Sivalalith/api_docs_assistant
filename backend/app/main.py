from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.documents import router as documents_router
from app.api.query import router as query_router

app = FastAPI(title="API Documents Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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