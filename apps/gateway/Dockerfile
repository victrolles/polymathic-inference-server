FROM python:3.12-slim

WORKDIR /app

# PYTHONPATH=/app → package "app" is /app/app/, "python" is /app/python/
COPY apps/gateway/app ./app
COPY libs/python ./python
COPY apps/gateway/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
