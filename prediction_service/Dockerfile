FROM python:3.9.12

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install evidently

COPY app.py . 
COPY model.pkl .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9696"]
