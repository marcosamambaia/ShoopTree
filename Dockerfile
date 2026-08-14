FROM python:3.11-slim
WORKDIR /app

COPY ./shoop_api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./shoop_api ./shoop_api
COPY ./simulacao_eventos ./simulacao_eventos

CMD ["uvicorn", "shoop_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
