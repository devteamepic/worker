import pika
from proto_types_pb2 import Document
import os
import utils

print('HUY', os.environ['AMQP_URL'], os.environ['RABBITMQ_DEFAULT_USER'],
                                  os.environ['RABBITMQ_DEFAULT_PASS'])
pika.credentials.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'],
                                  os.environ['RABBITMQ_DEFAULT_PASS'], erase_on_connect=False)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['AMQP_URL']))

channel = connection.channel()

channel.queue_declare(queue='documents_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    doc = Document()
    doc.ParseFromString(body)
    #utils.download(doc.file)
    # TODO
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='documents_queue', on_message_callback=callback)

channel.start_consuming()