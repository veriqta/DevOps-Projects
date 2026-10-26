FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -u 10001 orders
COPY server.py .
USER orders
CMD ["python", "server.py"]
