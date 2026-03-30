FROM python:3.12-slim

WORKDIR /app

ENV MODEL_ID=unknown

COPY apps/media_service/app ./app
COPY libs/python ./python
COPY models/${MODEL_ID} ./models/${MODEL_ID}
COPY apps/media_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt && \
    if [ -f "./models/${MODEL_ID}/requirements/inference.txt" ]; then \
      pip install --no-cache-dir -r "./models/${MODEL_ID}/requirements/inference.txt"; \
    fi

ENV PYTHONPATH=/app

EXPOSE 6000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6000"]