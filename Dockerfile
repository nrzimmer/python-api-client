FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT [ "python", "./client.py" ] 
