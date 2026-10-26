FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
RUN adduser -D -u 10001 service
USER service
CMD ["python", "server.py"]
