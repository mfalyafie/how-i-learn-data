FROM python:3.7.6

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        file \
        gcc  \
        libwww-perl \
        libffi-dev \
        make && \
    pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get autoremove -y && apt-get clean && rm /var/lib/apt/lists/*_*

CMD uvicorn --host=0.0.0.0 main:app