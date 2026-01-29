FROM --platform=$BUILDPLATFORM python:latest

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py", "--web"]
