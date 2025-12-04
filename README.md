# ELK + FastAPI Logging Demo (Elasticsearch 9 + Kibana + Logstash)

یک پروژه کامل، تمیز و آماده تولید برای ارسال لاگ‌های FastAPI به استک ELK با استفاده از TCP + JSON.

تمامی مشکلات رایج Elasticsearch 9.x و Kibana 9.x (مثل service account token و import error) حل شده.

## ویژگی‌ها
- Elasticsearch 9.2.1 با امنیت فعال
- Kibana 9.2.1 با ترفند service token برای محیط توسعه
- Logstash با ورودی TCP + `json_lines`
- heartbeat    بررسی سلامت سرویس ها
- service-loanResource    سرویس app 
- service-payment   سرویس app
- service-reservation   سرویس app
- common   لاگر مشترک برای سرویس ها
- لاگ‌های استاندارد JSON با `@timestamp` درست
- 
- کاملاً با Docker Compose

## شروع سریع

```bash
git clone https://github.com/yourname/elk-fastapi-logging-demo.git
cd elk-fastapi-logging-demo
docker compose up --build
