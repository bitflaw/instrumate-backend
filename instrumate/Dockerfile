FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt_tab


COPY migrations.sh .

RUN chmod +x migrations.sh

RUN ./migrations.sh

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]