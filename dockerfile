FROM python:3.9-slim as base

FROM base as builder

RUN ["mkdir", "/install"]
WORKDIR /install
COPY app/requirements.txt /requirements.txt
RUN ["pip", "install", "--prefix=/install", "--no-cache-dir", "-r", "/requirements.txt"]

FROM base

COPY --from=builder /install /usr/local
COPY app/ /app
WORKDIR /app

ENTRYPOINT ["python3", "main.py"]
