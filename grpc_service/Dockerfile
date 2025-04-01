FROM python:3.10

WORKDIR /app

COPY ./src /app/src
COPY ./proto/posts_service.proto /app/
COPY ./requirements.txt /app/requirements.txt

ENV PYTHONPATH="/app/src"

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "src/main.py"]
