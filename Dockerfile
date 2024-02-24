FROM python:slim-bullseye
WORKDIR /app
RUN apt-get update && \
    apt-get install -y procps curl vim
ENV TZ Asia/Shanghai
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["python3", "/app/web.py"]
