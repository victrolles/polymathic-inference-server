FROM python:3.12-slim

WORKDIR /app

ENV MODELS_PATH=/app/models

COPY apps/media_service/app ./app
COPY libs/python ./python
COPY models ./models
COPY apps/media_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt && \
    for model in ./models/*; do \
      if [ -f "$model/requirements/pipeline.txt" ]; then \
        pip install --no-cache-dir -r "$model/requirements/pipeline.txt"; \
      fi; \
    done

ENV PYTHONPATH=/app

EXPOSE 7000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]