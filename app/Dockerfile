FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py
COPY ./data/starlink_historical_data.json ./data/starlink_historical_data.json
CMD ["python", "-u", "app.py"]
