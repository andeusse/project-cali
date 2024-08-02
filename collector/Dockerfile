FROM python:3.11.9-slim-bullseye

WORKDIR /app

# add app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# start app
CMD ["python", "Collector.py"]
