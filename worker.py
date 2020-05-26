import pika
from proto_types_pb2 import Document, DocumentsSubmission
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import os
import sseclient
import requests
import json
import utils
import numpy as np

# ENCODED_ABSTRACTS_URL = os.environ['ENCODED_ABSTRACTS_URL']

creds = pika.credentials.PlainCredentials(
    os.environ['RABBITMQ_DEFAULT_USER'],
    os.environ['RABBITMQ_DEFAULT_PASS'], erase_on_connect=False
)


def get_data():
    with open('submissions.json') as f:
        data = json.loads(f.read())
        # print(data[0]['id'])
        # print(data[0]['encoded_abstract']['tokens'])
    return np.asarray(data)

data = get_data()

# print(data[0])

# print(len(data))

connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['AMQP_URL'],
                                                               credentials=creds))



channel = connection.channel()

channel.queue_declare(queue='documents_queue', durable=True)

# print(type(np.asarray(data[0]['encoded_abstract']['tokens'], dtype=np.float32)))

print(' [*] Waiting for messages. To exit press CTRL+C')

bert_client = BertClient(ip="bert-server")

abstract = np.asarray(bert_client.encode(test, show_tokens=False, is_tokenized=False))

cos_sim = cosine_similarity(abstract.reshape(1,-1), np.asarray(data[0]['encoded_abstract']['tokens'], dtype=np.float32).reshape(1,-1))

def callback(ch, method, properties, body):

    submission = DocumentsSubmission()
    submission.ParseFromString(body)
    print(submission.abstract)
    
    authors = []
    similarities = []

    bert_client = BertClient(ip="bert-server")

    abstract = bert_client.encode(submission.abstract, show_tokens=False, is_tokenized=False)

    print(abstract)

    for i in range(len(data)):
        cur_vector = np.asarray(data[i]['encoded_abstract']['tokens'], dtype=np.float32)
        cur_id = data[i]['id']
        cos_sim = cosine_similarity(abstract.reshape(1,-1), cur_vector.reshape(1,-1))
        
        authors.append(cur_id)
        similarities.append(-cos_sim)

    result = [x for _, x in sorted(zip(similarities, authors))]
    
    result = result[:5]

    res = requests.post(f"worker_api/v1/submissions/{submission.id}",
                        headers={f"{os.environ['SECRET_HEADER']}": os.environ['SECRET_TOKEN']},
                        json={'professor_submission_ids': result})

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='documents_queue', on_message_callback=callback)

channel.start_consuming()
