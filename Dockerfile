FROM python:3

WORKDIR /home/paydaylight/PycharmProjects/worker

RUN curl https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip --output model.zip
RUN unzip ./model.zip -d ./bert/
RUN rm ./model.zip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./worker.py" ]