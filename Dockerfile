FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client \
    gcc \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* # Очистка кэша apt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

COPY --chmod=755 entrypoint.sh /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
