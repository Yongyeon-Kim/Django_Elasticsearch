FROM python:3.10-slim AS lite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt .
COPY wait-for-it.sh /wait-for-it.sh
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x /wait-for-it.sh
COPY . .