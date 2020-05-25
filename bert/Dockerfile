FROM tensorflow/tensorflow:1.10.0-py3

WORKDIR /app

RUN pip install bert-serving-server[http]

RUN curl https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip --output model.zip
RUN unzip ./model.zip -d /model/
RUN rm ./model.zip

COPY ./entrypoint.sh /app

USER root
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
#HEALTHCHECK --timeout=5s CMD curl -f http://localhost:8125/status/server || exit 1