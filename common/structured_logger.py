import logging
import socket
import json
import uuid
import threading
import os
from datetime import datetime
from pytz import timezone
from fastapi import Request

# تنظیمات زمانی تهران
TEHRAN_TZ = timezone('Asia/Tehran')
thread_local = threading.local()

def get_transaction_id():
    """هر درخواست یه transactionId منحصر به فرد داشته باشه"""
    if not hasattr(thread_local, "transaction_id"):
        thread_local.transaction_id = str(uuid.uuid4())
    return thread_local.transaction_id

# دسته‌بندی کامل (شامل Info و Error)
CATEGORY_MAPPING = {
    "system": "SystemError",        # خطاهای زیرساختی (دیتابیس، شبکه، Redis و ...)
    "business": "BusinessError",    # خطاهای کسب‌وکاری (موجودی، اعتبار، دسترسی و ...)
    "application": "ApplicationError",  # خطاهای برنامه‌نویسی (Null، 500، Exception)
    "info": "ApplicationInfo",      # لاگ‌های موفق و اطلاع‌رسانی
    "warning": "ApplicationWarning", # هشدارهای برنامه‌ای
}

# تبدیل سطح لاگ
LOG_LEVELS = {
    logging.ERROR: "Error",
    logging.WARNING: "Warn",
    logging.INFO: "Info",
    logging.DEBUG: "Debug",
}

class StructuredLogHandler(logging.Handler):
    def __init__(self, app_name: str, env: str):
        super().__init__()
        self.app_name = app_name
        self.env = env

    def emit(self, record):
        try:
            now = datetime.now(TEHRAN_TZ)
            # فرمت ISO8601 با آفست تهران (مثل: 2025-12-02T14:30:25.123+03:30)
            timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + now.strftime('%z')
            if timestamp[-5] != ':':
                timestamp = timestamp[:-2] + ':' + timestamp[-2:]

            # تعیین دسته‌بندی هوشمند
            if hasattr(record, 'category') and getattr(record, 'category', None):
                category_key = record.category
            elif record.levelno >= logging.ERROR:
                category_key = "application"   # خطاهای بدون دسته → ApplicationError
            elif record.levelno == logging.WARNING:
                category_key = "warning"
            else:  # INFO و DEBUG
                category_key = "info"

            category = CATEGORY_MAPPING.get(category_key, "ApplicationInfo")

            # سطح لاگ
            level_name = LOG_LEVELS.get(record.levelno, "Info")

            log_entry = {
                "@timestamp": timestamp,
                "app": self.app_name,
                "env": self.env,
                "transactionId": get_transaction_id(),
                "errorCategory": category,
                "logLevel": level_name,
                "level": record.levelname,
                "message": record.getMessage(),
                "logger_name": record.name,
                "host": socket.gethostname(),
                "thread_name": threading.current_thread().name
            }

            # اگر استثناء بود، جزئیات کامل رو اضافه کن
            if record.exc_info:
                log_entry["stacktrace"] = logging.Formatter().formatException(record.exc_info)
                log_entry["exception"] = str(record.exc_info[1]) if record.exc_info[1] else "Unknown"

            # ارسال به Logstash
            msg = json.dumps(log_entry, ensure_ascii=False) + "\n"
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(("logstash", 5044))
            sock.sendall(msg.encode("utf-8"))
            sock.close()
        except Exception:
            # اگر ارسال به Logstash هم شکست، حداقل تو docker logs بمونه
            pass

def setup_logger(app_name: str, env: str = "dev"):
    """تنظیم لاگر برای هر سرویس"""
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    if not any(isinstance(h, StructuredLogHandler) for h in logger.handlers):
        logger.addHandler(StructuredLogHandler(app_name, env))
        logger.addHandler(logging.StreamHandler())

    return logger

# توابع کمکی برای دسته‌بندی درست
def app_info(logger, message, *args, **kwargs):
    """لاگ‌های موفق و اطلاع‌رسانی → ApplicationInfo"""
    kwargs.setdefault('extra', {})['category'] = 'info'
    logger.info(message, *args, **kwargs)

def app_warning(logger, message, *args, **kwargs):
    """هشدارهای برنامه‌ای → ApplicationWarning"""
    kwargs.setdefault('extra', {})['category'] = 'warning'
    logger.warning(message, *args, **kwargs)

def business_error(logger, message, *args, **kwargs):
    """خطاهای کسب‌وکاری → BusinessError"""
    kwargs.setdefault('extra', {})['category'] = 'business'
    logger.error(message, *args, **kwargs)

def system_error(logger, message, *args, **kwargs):
    """خطاهای سیستمی → SystemError"""
    kwargs.setdefault('extra', {})['category'] = 'system'
    logger.error(message, *args, **kwargs)

# میدلوِر برای transactionId
async def transaction_middleware(request: Request, call_next):
    thread_local.transaction_id = str(uuid.uuid4())
    response = await call_next(request)
    return response
