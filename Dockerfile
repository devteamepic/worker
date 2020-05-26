FROM python:3

WORKDIR ./worker

RUN curl https://unifound.me/files/submissions.json --output submissions.json

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./worker.py" ]