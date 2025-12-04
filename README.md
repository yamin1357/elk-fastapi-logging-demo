# میکروسرویس‌های FastAPI + ELK Stack + Observability کامل (2025)

یک پروژه **کاملاً واقعی و پروداکشن-ریدی** برای مانیتورینگ و لاگینگ میکروسرویس‌ها با استفاده از:

- **FastAPI** (۳ سرویس مستقل)
- **ELK Stack** (Elasticsearch + Logstash + Kibana 9.2.1)
- **Heartbeat** برای مانیتورینگ سلامت سرویس‌ها
- **Structured Logging** با دسته‌بندی هوشمند خطاها
- **Docker Compose** + ایمیج جدا برای هر سرویس

> این پروژه دقیقاً همون چیزیه که تو شرکت‌های بزرگ مثل اسنپ، دیجی‌کالا، آپارات و ... استفاده می‌شه.

## ویژگی‌های کلیدی

| قابلیت                         | وضعیت       | توضیحات |
|-------------------------------|-------------|--------|
| لاگینگ ساختاریافته JSON      | ✅ انجام شد | زمان تهران + transactionId + stacktrace |
| دسته‌بندی خطا                  | ✅ انجام شد | `ApplicationInfo`, `ApplicationError`, `BusinessError`, `SystemError` |
| مانیتورینگ سلامت سرویس‌ها       | ✅ انجام شد | Heartbeat هر ۱۰ ثانیه چک می‌کنه |
| داشبورد زنده در Kibana         | ✅ انجام شد | آپتایم، latency، وضعیت Up/Down |
| ایمیج جداگانه برای هر سرویس     | ✅ انجام شد | بدون rebuild در هر اجرا |
| شبکه داخلی و volume           | ✅ انجام شد | استاندارد پروداکشن |
| آماده برای Alerting            | ✅ آماده     | تلگرام، اسلک، ایمیل (فقط یه خط اضافه کن!) |

## ساختار پروژه
.
├── common/                     مشترک برای همه سرویس‌ها
│   └── structured_logger.py    لاگر هوشمند با دسته‌بندی خطا
├── service-loanResource/       سرویس وام
├── service-payment/            سرویس پرداخت
├── service-reservation/        سرویس رزرو
├── logstash/                   تنظیمات Logstash (با volume)
├── heartbeat/                  مانیتورینگ سلامت سرویس‌ها
├── docker-compose.yml
└── README.md



## شروع سریع

```bash
# کلون کن
git clone https://github.com/username/elk-fastapi-observability.git
cd elk-fastapi-observability

# بالا بیار (اولین بار ~۲ دقیقه، بعدش ~۱۰ ثانیه!)
docker compose up -d --build

# یا فقط آپدیت کن (بدون rebuild)
docker compose up -d

# درخواست موفق → ApplicationInfo
curl http://localhost:8002/

# خطای برنامه‌نویسی → ApplicationError
curl http://localhost:8002/app-error

# خطای کسب‌وکاری → BusinessError
curl http://localhost:8002/business-error

# خطای سیستمی → SystemError
curl http://localhost:8002/system-error
