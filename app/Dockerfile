FROM python:3.11
WORKDIR /app
COPY requirements.txt /app/app/requirements.txt
COPY main.py /app/
RUN pip install --upgrade pip &&  pip install --no-cache-dir --upgrade -r /app/app/requirements.txt
RUN groupadd --gid 2000 worker \
  && useradd --uid 2000 --gid worker --shell /bin/bash --create-home worker
USER worker
