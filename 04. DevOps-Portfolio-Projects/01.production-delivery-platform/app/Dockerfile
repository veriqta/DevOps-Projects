FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
RUN adduser -D -u 10001 orders
USER orders
EXPOSE 8080
CMD ["python", "server.py"]
