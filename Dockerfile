FROM python:3

WORKDIR ./worker

RUN curl https://drive.google.com/open?id=1V_WMWXnaNs350MSiNJEihfEafujYqIlp --output submissions.json

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./worker.py" ]