FROM python:3.9.14-slim

COPY src/stream_processing/requirements.txt app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r app/requirements.txt

COPY src/ /app/src/
COPY utils/ /app/utils/

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENTRYPOINT [ "python", "-m", "bytewax.run", "src/stream_processing/dataflow.py" ]