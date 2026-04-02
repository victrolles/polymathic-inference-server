FROM nvidia/cuda:13.1.1-runtime-ubuntu22.04
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

ENV MODELS_PATH=/app/models

COPY apps/worker/app ./app
COPY libs/python ./python
COPY models ./models
COPY apps/worker/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt && \
    for model in ./models/*; do \
      if [ -f "$model/requirements/inference.txt" ]; then \
        pip install --no-cache-dir -r "$model/requirements/inference.txt"; \
      fi; \
    done

ENV PYTHONPATH=/app

EXPOSE 6000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6000"]