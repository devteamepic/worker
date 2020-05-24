#!/bin/sh
bert-serving-start -http_port 8125 -num_worker=1 -model_dir /model/uncased_L-12_H-768_A-12/ -cpu -max_batch_size 16