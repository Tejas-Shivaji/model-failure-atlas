import os

APP_NAME = "Model-Failure Atlas API"
APP_VERSION = "1.0.0"
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
MAX_ROWS = int(os.getenv("MAX_ROWS", "100000"))
MAX_COLUMNS = int(os.getenv("MAX_COLUMNS", "100"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./model_failure_atlas.db")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
