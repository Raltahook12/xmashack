FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]
