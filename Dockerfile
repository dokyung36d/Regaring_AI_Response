FROM python:latest

WORKDIR /app

COPY requirements.txt .
 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn --host=0.0.0.0 --port 8000 app.main:app

 
# COPY ./app /code/app
 