FROM python:3.9.14-slim

COPY src/producer/requirements.txt app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r app/requirements.txt
RUN apt-get update && apt-get install -y iputils-ping

COPY src/ /app/src/
COPY utils/ /app/utils/

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENTRYPOINT [ "python", "src/producer/producer.py" ]