FROM python:3.11.9-slim-bullseye

WORKDIR /app

# add app
COPY . .

RUN pip install --no-cache-dir -r v1.0/requirements.txt

EXPOSE 5000

# start app
CMD ["python", "v1.0/main.py"]
