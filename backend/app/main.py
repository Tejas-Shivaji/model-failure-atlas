from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_NAME, APP_VERSION, ALLOWED_ORIGINS
from app.database import Base, engine
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Investigate classification model performance, data slices and prediction errors.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/api/health")
def health():
    return {"status": "ok", "name": APP_NAME, "version": APP_VERSION,
            "storage": "bounded process memory for uploaded datasets; SQL database for saved investigations"}
