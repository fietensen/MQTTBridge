FROM python:3.11

WORKDIR /mqtt_proxy

COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m unittest discover tests

ENTRYPOINT [ "python", "./src/main.py" ]