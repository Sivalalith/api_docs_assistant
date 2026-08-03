from fastapi import FastAPI

app = FastAPI(title="API Documents Assistant")


@app.get("/")
def root():
    return {
        "message": "API Documents Assistant Backend Running"
    }