FROM python:3.7-slim 
 
WORKDIR /app 
 
COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
 
LABEL author='andrespa_90@hotmail.com' version=1 broken_keyboards=5
 
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
