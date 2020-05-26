import pika
from bert_serving.client import BertClient
import os
import sseclient
import requests
import json
from proto_types_pb2 import Document, DocumentsSubmission


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
    print("starting request to backend")
    submission = DocumentsSubmission()
    submission.ParseFromString(body)
    print(submission)
    print(submission.id)
    encoded_abstract = bert_client.encode([submission.abstract])
    res = requests.post(f"{GET_PROF_ABSTRACTS}/{submission.id}/encoded",
                        headers={f"{os.environ['SECRET_HEADER']}": os.environ['SECRET_TOKEN']},
                        json={'tokens_array': encoded_abstract.tolist()})
    print(res)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='documents_encode', on_message_callback=callback)

channel.start_consuming()