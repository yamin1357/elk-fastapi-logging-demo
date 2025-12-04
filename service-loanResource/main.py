from fastapi import FastAPI
import os
from common.structured_logger import (
    setup_logger, transaction_middleware,
    app_info, business_error, system_error
)

app = FastAPI()
app.middleware("http")(transaction_middleware)

APP_NAME = os.getenv("APP_NAME", "unknown")
logger = setup_logger(APP_NAME, os.getenv("ENV", "dev"))

@app.get("/")
async def home():
    app_info(logger, "درخواست موفق به سرویس")  # → ApplicationInfo
    return {"service": APP_NAME, "status": "ok"}

@app.get("/business-error")
async def test_business():
    business_error(logger, "موجودی کافی نیست")  # → BusinessError
    return {"status": "failed"}

@app.get("/system-error")
async def test_system():
    system_error(logger, "دیتابیس قطع شد")  # → SystemError
    return {"status": "failed"}

@app.get("/app-error")
async def test_app():
    try:
        1 / 0
    except Exception:
        logger.exception("خطای برنامه‌نویسی")  # → ApplicationError
    return {"status": "error"}
