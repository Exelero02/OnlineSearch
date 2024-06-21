FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y python3-tk x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:0

CMD ["python", "./wikipedia_search_app.py"]
