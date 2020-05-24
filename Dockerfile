FROM python:3

WORKDIR ./worker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./worker.py" ]