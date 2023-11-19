FROM python:3.10
LABEL authors="Marildo César"

WORKDIR /env
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools   \
    && pip install --upgrade pip   \
    && pip install --no-cache-dir -r requirements.txt


# docker build -t env-tdc .    