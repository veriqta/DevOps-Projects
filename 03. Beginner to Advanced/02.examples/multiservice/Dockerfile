FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
RUN adduser -D -u 10001 lab && mkdir /data && chown lab /data
USER lab
CMD ["python", "app.py"]
