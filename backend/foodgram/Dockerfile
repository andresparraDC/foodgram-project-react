FROM python:3.7-slim 
 
WORKDIR /app 
 
COPY . .

RUN pip install -r .requirements.txt
 
LABEL author='andrespa_90@hotmail.com' version=1 broken_keyboards=5
 
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
