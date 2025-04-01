FROM python:3.10

WORKDIR /app

COPY base_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["uvicorn", "base_service.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]
