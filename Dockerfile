FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY reports/sql ./reports/sql

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.pipeline"]