FROM python:3

WORKDIR ./encoder

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./encoder.py" ]