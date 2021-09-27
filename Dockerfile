FROM python:3.9
WORKDIR /code
COPY dev_server.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "./dev_server.py" ]