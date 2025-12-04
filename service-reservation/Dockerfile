FROM python:3.11-slim
WORKDIR /app
COPY service-reservation/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY service-reservation/main.py ./main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
