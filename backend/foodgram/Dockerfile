FROM python:3.7-slim 
 
WORKDIR /app 

RUN pip install --upgrade pip

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

LABEL author='andrespa_90@hotmail.com' version=1 broken_keyboards=5
 
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
