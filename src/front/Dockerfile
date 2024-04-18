FROM python:3.9.14-slim

COPY src/front/requirements.txt app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r app/requirements.txt

COPY src/ /app/src/
COPY utils/ /app/utils/

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENTRYPOINT [ "streamlit", "run", "src/front/front.py", "--server.port=8501", "--server.address=0.0.0.0" ]
