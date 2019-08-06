FROM python:latest

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
