FROM python:alpine3.14

COPY * ./

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
