import pika
from bert_serving.client import BertClient
import os
import sseclient
import requests
import json


GET_PROF_ABSTRACTS = os.environ['GET_PROFS_SUBMISSIONS_URL']

creds = pika.credentials.PlainCredentials(
    os.environ['RABBITMQ_DEFAULT_USER'],
    os.environ['RABBITMQ_DEFAULT_PASS'], erase_on_connect=False
)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['AMQP_URL'],
                                                               credentials=creds))

channel = connection.channel()

channel.queue_declare(queue='documents_encode', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    bert_client = BertClient(ip="bert-server")

    abstracts_response = requests.get(GET_PROF_ABSTRACTS,
                                      stream=True,
                                      headers={f"{os.environ['SECRET_HEADER']}": os.environ['SECRET_TOKEN']})
    client = sseclient.SSEClient(abstracts_response)
    for event in client.events():
        print(json.loads(event.data))

    # works fine
    # print(bert_client.encode([submission.abstract]))

    # TODO
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='documents_queue', on_message_callback=callback)

channel.start_consuming()